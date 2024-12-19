from arches.app.search.search_export import SearchResultsExporter
from django.db import connection
from arches.app.models import models
from bcrhp.util.bcrhp_aliases import GraphSlugs


class BCRHPSearchResultsExporter(SearchResultsExporter):
    _heritage_site_nodegroups = None

    def flatten_tiles(self, tiles, datatype_factory, compact=True, use_fieldname=False):

        if not self._heritage_site_nodegroups:
            graph = models.GraphModel.objects.get(slug=GraphSlugs.HERITAGE_SITE)
            nodes = (
                models.Node.objects.filter(graph=graph)
                .exclude(nodegroup__isnull=True)
                .all()
            )
            self._heritage_site_nodegroups = set()
            for node in nodes:
                self._heritage_site_nodegroups.add(str(node.nodegroup.nodegroupid))

        feature_collections = {}
        compacted_data = {}
        lookup = {}
        has_geometry = False

        is_heritage_site = (
            next((x["nodegroup_id"] for x in tiles if x["nodegroup_id"]), None)
            in self._heritage_site_nodegroups
        )

        for tile in tiles:  # normalize tile.data to use labels instead of node ids
            compacted_data["resourceid"] = tile["resourceinstance_id"]
            for nodeid, value in tile["data"].items():
                node = self.get_node(nodeid)
                if node.exportable or (
                    is_heritage_site
                    and node.datatype != "semantic"
                    and self.search_request.user.is_superuser
                ):
                    datatype = datatype_factory.get_instance(node.datatype)
                    node_value = datatype.get_display_value(tile, node)
                    label = node.fieldname if use_fieldname is True else node.name

                    if compact:
                        if node.datatype == "geojson-feature-collection" and node_value:
                            has_geometry = True
                            feature_collections = self.get_feature_collections(
                                tile, node, feature_collections, label, datatype
                            )
                        else:
                            try:
                                compacted_data[label] += ", " + str(node_value)
                            except KeyError:
                                compacted_data[label] = str(node_value)
                    else:
                        data[label] = str(node_value)

            if (
                not compact
            ):  # add on the cardinality and card_names to the tile for use later on
                tile["data"] = data
                card = models.CardModel.objects.get(nodegroup=tile["nodegroup_id"])
                tile["card_name"] = card.name
                tile["cardinality"] = node.nodegroup.cardinality
                tile[card.name] = tile["data"]
                lookup[tile["tileid"]] = tile
        if compact:
            for key, value in feature_collections.items():
                compacted_data[key] = value["datatype"].transform_export_values(value)
            compacted_data["has_geometry"] = has_geometry
            return compacted_data

        resource_json = self.create_resource_json(tiles)
        return flatten_dict(resource_json)

    def to_csv(self, instances, headers, name):
        if name == "Heritage Site":
            if (
                self.search_request.user.username == "anonymous"
            ):  # Anonymous users use the view
                collection_ids = [o["resourceid"] for o in instances]

                with connection.cursor() as cur:
                    cur.execute(
                        """
                        select *
                        from heritage_site.csv_export
                        where array_position(%s, site_id::text) is not null
                    """,
                        [collection_ids],
                    )
                    columns = [desc[0] for desc in cur.description]
                    results = [dict(zip(columns, row)) for row in cur.fetchall()]
                    return super().to_csv(results, columns, name)
            else:  # We're an authenticated user - show all the nodes
                has_report_link = len(instances) > 0 and "Link" in instances[0]
                graph = models.GraphModel.objects.get(slug=GraphSlugs.HERITAGE_SITE)
                headers = self.return_ordered_header_for_all(graph.graphid)
                headers.append("resourceid")
                if has_report_link and ("Link" not in headers):
                    headers.append("Link")
                print("First row: %s" % instances[0])
                return super().to_csv(instances, headers, name)

        return super().to_csv(instances, headers, name)

    def return_ordered_header_for_all(self, graphid):
        # Copy of the SearchResultsExporter.return_ordered_header() function without filtering by exportable=True

        subcard_list_with_sort = []
        all_cards = models.CardModel.objects.filter(graph=graphid).prefetch_related(
            "nodegroup"
        )
        all_card_list_with_sort = list(
            all_cards.exclude(sortorder=None).order_by("sortorder")
        )
        card_list_no_sort = list(all_cards.filter(sortorder=None))
        sorted_card_list = []

        # Work out which cards with sort order are sub cards by looking at the
        # related nodegroup's parent nodegroup value

        for card_with_sortorder in all_card_list_with_sort:
            if card_with_sortorder.nodegroup.parentnodegroup_id is None:
                sorted_card_list.append(card_with_sortorder)
            else:
                subcard_list_with_sort.append(card_with_sortorder)

        # Reverse set to allow cards with sort and a parent nodegroup
        # to be injected into the main list in the correct order i.e. above
        # cards with no sort order and according to the sort order as cards are
        # injected just below the top card.

        subcard_list_with_sort.sort(key=lambda x: x.sortorder, reverse=True)

        def order_cards(subcards_added=True):
            if subcards_added == True:
                subcards_added = False
                unsorted_subcards_added = self.insert_subcard_below_parent_card(
                    sorted_card_list, card_list_no_sort, subcards_added
                )
                sorted_subcards_added = self.insert_subcard_below_parent_card(
                    sorted_card_list, subcard_list_with_sort, unsorted_subcards_added
                )
                order_cards(sorted_subcards_added)

        order_cards()

        # Create a list of nodes within each card and order them according to sort
        # order then add them to the main list of

        ordered_list_all_nodes = []
        for sorted_card in sorted_card_list:
            card_node_objects = list(
                models.CardXNodeXWidget.objects.filter(
                    card_id=sorted_card.cardid
                ).prefetch_related("node")
            )
            if len(card_node_objects) > 0:
                nodes_in_card = []
                for card_node_object in card_node_objects:
                    if card_node_object.node.datatype != "semantic":
                        nodes_in_card.append(card_node_object)
                node_object_list_sorted = sorted(
                    nodes_in_card, key=lambda x: x.sortorder
                )
                for sorted_node_object in node_object_list_sorted:
                    ordered_list_all_nodes.append(sorted_node_object)

        # Build the list of headers (in correct format for return file format) to be returned
        # from the ordered list of nodes, only where the exportable tag is true

        headers = []
        node_id_list = []
        for ordered_node in ordered_list_all_nodes:
            node_object = ordered_node.node
            if node_object.nodeid not in node_id_list:
                headers.append(node_object.name)
                node_id_list.append(node_object.nodeid)

        return headers
