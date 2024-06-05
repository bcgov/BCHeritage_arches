from arches.app.datatypes import datatypes, concept_types
from arches.app.search.elasticsearch_dsl_builder import Bool, Ids, Match, Nested, SimpleQueryString, QueryString, Terms, Term
from bcfms.util.bcfms_aliases import CollectionEventAliases, FossilSampleAliases, GraphSlugs
from bcfms.util.scientific_terms_util import ScientificTermsFormatter


class CustomSearchValue:
    custom_search_path = "custom_values"

    def __init__(self):
        pass

    @staticmethod
    def add_search_terms(resourceinstance, document, terms):
        import arches.app.models.tile as tile
        from arches.app.models.models import Node, GraphModel
        # print("Resource Instance: %s" % resourceinstance)
        # print("Resource Instance Graph: %s" % resourceinstance.graph)
        # print("Terms: %s" % str(terms))
        custom_values = []

        if resourceinstance.graph.slug == GraphSlugs.COLLECTION_EVENT:
            sample_graph = GraphModel.objects.filter(slug='fossil_sample', isresource=True).first()
            resource_dt = datatypes.ResourceInstanceDataType()
            concept_dt = concept_types.ConceptDataType()
            resourceinstance.load_tiles()
            sample_node = Node.objects.filter(alias=CollectionEventAliases.SAMPLES_COLLECTED).first()
            # print("Node values: %s" % str(resourceinstance.get_node_values(sample_node.name)))
            samples = resourceinstance.get_node_values(sample_node.name)
            # print("Samples: %s" % samples)
            # print("Resource Instance Tiles: %s" % resourceinstance.tiles)
            if samples and len(samples) > 0:
                custom_values = set(())
                document[CustomSearchValue.custom_search_path] = []
                scientific_name_node = Node.objects.filter(alias=FossilSampleAliases.SCIENTIFIC_NAME).first()
                conn_node = Node.objects.filter(alias=FossilSampleAliases.NAME_CONNECTOR).first()
                other_name_node = Node.objects.filter(alias=FossilSampleAliases.OTHER_SCIENTIFIC_NAME).first()
                common_name_node = Node.objects.filter(alias=FossilSampleAliases.FOSSIL_COMMON_NAME).first()
                # print("sample_node graph ID: %s" % sample_node.graph.graphid)
                minimum_time_node = Node.objects.filter(alias=FossilSampleAliases.MINIMUM_TIME, graph__graphid=sample_graph.graphid).first()
                # print("Minimum_time_node: %s" % minimum_time_node)
                maximum_time_node = Node.objects.filter(alias=FossilSampleAliases.MAXIMUM_TIME, graph__graphid=sample_graph.graphid).first()
                # print("Maximum_time_node: %s" % maximum_time_node)
                for sample in samples:
                    # print("Sample: %s" % sample)
                    related_tiles = tile.Tile.objects.filter(resourceinstance_id=sample["resourceId"],
                                                            nodegroup__nodegroupid=scientific_name_node.nodegroup_id).all()
                    # print("Related tile: %s" % sample)
                    for related_tile in related_tiles:
                        sci_name_val = resource_dt.get_display_value(related_tile, scientific_name_node)
                        conn_val = concept_dt.get_display_value(related_tile, conn_node)
                        other_name_val = resource_dt.get_display_value(related_tile, other_name_node)
                        name_val = ScientificTermsFormatter.format_scientific_name(sci_name_val, conn_val, other_name_val)
                        common_val = resource_dt.get_display_value(related_tile, common_name_node)
                        custom_values.add(name_val)
                        custom_values.add(common_val)
                        # print("Related node value: %s" % name_val)
                        # document[CustomSearchValue.custom_search_path].append({"custom_value": name_val})

                    related_tiles = tile.Tile.objects.filter(resourceinstance_id=sample["resourceId"],
                                                             nodegroup__nodegroupid=minimum_time_node.nodegroup_id).all()
                    # print("Number of times(%s,%s): %s" %( sample["resourceId"], minimum_time_node.nodegroup_id, len(related_tiles)))
                    for related_tile in related_tiles:
                        custom_values.add(concept_dt.get_display_value(related_tile, minimum_time_node))
                        custom_values.add(concept_dt.get_display_value(related_tile, maximum_time_node))

                for custom_value in custom_values:
                    if custom_value:
                        # print("Related node value: %s" % custom_value)
                        document[CustomSearchValue.custom_search_path].append({"custom_value": custom_value})
            # else:
            #     # dt.get_tile_data()
            #     print("Document Before: %s" % document)
            #     # document["strings"].append({"string": "hello",   "nodegroup_id": ["c047fab8-0ee5-11ef-a3ec-0242ac120009"], "provisional": [False ],})
            #     # document["strings"].append({"string": "hello2",   "nodegroup_id": ["00000000-0000-0000-0000-000000000000"], "provisional": [False],})
            #
            #     document[CustomSearchValue.custom_search_path] = [{"custom_value": "hello2"}]
            #     print("Document After: %s" % document)

    @staticmethod
    def add_search_filter(search_query, term):

        print("Search query before: %s" % search_query)
        # print("Search query type: %s" % type(search_query))
        # print("DSL type: %s" % type(search_query.dsl))

        search_query.dsl["bool"]["should"] = search_query.dsl["bool"]["must"]
        search_query.dsl["bool"]["must"] = []
        search_query.dsl["bool"]["minimum_should_match"] = 1

        document_key = CustomSearchValue.custom_search_path
        custom_filter = Bool()
        custom_filter.should(Match(field="%s.custom_value" % document_key, query=term["value"], type="phrase_prefix"))
        custom_filter.should(Match(field="%s.custom_value.folded" % document_key, query=term["value"], type="phrase_prefix"))
        nested_custom_filter = Nested(path=document_key, query=custom_filter)
        # return nested_custom_filter
        if term["inverted"]:
            search_query.must_not(nested_custom_filter)
        else:
            search_query.should(nested_custom_filter)
        print("Search query after: %s" % search_query)

    @staticmethod
    def get_custom_search_config():
        return {"type": "nested",
                "properties": {
                    "custom_value": {"type": "text",
                                     "fields": {
                                         "raw": {"type": "keyword", "ignore_above": 256},
                                         "folded": {"type": "text", "analyzer": "folding"}
                                     },
                                     }
                }
        }
