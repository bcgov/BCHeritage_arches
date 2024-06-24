from arches.app.datatypes import datatypes, concept_types
from arches.app.search.elasticsearch_dsl_builder import Bool, Ids, Match, Nested, SimpleQueryString, QueryString, Terms, Term
from bcfms.util.bcfms_aliases import CollectionEventAliases, FossilSampleAliases as fsa, FossilType, GraphSlugs
from bcfms.util.scientific_terms_util import ScientificTermsFormatter


class CustomSearchValue:
    custom_search_path = "custom_values"
    initialized = False
    sample_graph = None
    sample_node = None
    resource_dt = None
    concept_dt = None
    collection_event_nodes = {}
    sample_nodes = {}
    fossil_type_nodes = {}

    def __init__(self):
        pass

    @staticmethod
    def initialize():
        if not CustomSearchValue.initialized:
            from arches.app.models.models import Node, GraphModel
            CustomSearchValue.sample_graph = GraphModel.objects.filter(slug='fossil_sample', isresource=True).first()
            CustomSearchValue.resource_dt = datatypes.ResourceInstanceDataType()
            CustomSearchValue.concept_dt = concept_types.ConceptDataType()

            CustomSearchValue.collection_event_nodes[CollectionEventAliases.SAMPLES_COLLECTED] = Node.objects.filter(alias=CollectionEventAliases.SAMPLES_COLLECTED).first()

            CustomSearchValue.sample_nodes[fsa.SCIENTIFIC_NAME] = Node.objects.filter(alias=fsa.SCIENTIFIC_NAME).first()
            CustomSearchValue.sample_nodes[fsa.NAME_CONNECTOR] = Node.objects.filter(alias=fsa.NAME_CONNECTOR).first()
            CustomSearchValue.sample_nodes[fsa.OTHER_SCIENTIFIC_NAME] = Node.objects.filter(alias=fsa.OTHER_SCIENTIFIC_NAME).first()
            CustomSearchValue.sample_nodes[fsa.FOSSIL_COMMON_NAME] = Node.objects.filter(alias=fsa.FOSSIL_COMMON_NAME).first()
            CustomSearchValue.sample_nodes[fsa.MINIMUM_TIME] = Node.objects.filter(alias=fsa.MINIMUM_TIME).first()
            CustomSearchValue.sample_nodes[fsa.MAXIMUM_TIME] = Node.objects.filter(alias=fsa.MAXIMUM_TIME).first()

            CustomSearchValue.fossil_type_nodes[FossilType.NAME_TYPE] = Node.objects.filter(alias=FossilType.NAME_TYPE).first()
            CustomSearchValue.fossil_type_nodes[FossilType.PARENT_NAME] = Node.objects.filter(alias=FossilType.PARENT_NAME).first()


    @staticmethod
    def add_search_terms(resourceinstance, document, terms):
        CustomSearchValue.initialize()
        import arches.app.models.tile as tile
        custom_values = set(())

        # print("Slug: %s" % resourceinstance.graph.slug)
        if resourceinstance.graph.slug == GraphSlugs.COLLECTION_EVENT:
            resourceinstance.load_tiles()
            # print("Node values: %s" % str(resourceinstance.get_node_values(sample_node.name)))
            samples = resourceinstance.get_node_values(CustomSearchValue.collection_event_nodes[CollectionEventAliases.SAMPLES_COLLECTED].name)
            # print("Samples: %s" % samples)
            # print("Resource Instance Tiles: %s" % resourceinstance.tiles)
            if samples and len(samples) > 0:
                sample_nodes = CustomSearchValue.sample_nodes
                document[CustomSearchValue.custom_search_path] = []
                # print("Maximum_time_node: %s" % maximum_time_node)
                for sample in samples:
                    # print("Sample: %s" % sample)
                    custom_values.update(CustomSearchValue.get_fossil_types(sample))

                    related_tiles = tile.Tile.objects.filter(resourceinstance_id=sample["resourceId"],
                                                             nodegroup__nodegroupid=sample_nodes[fsa.MINIMUM_TIME].nodegroup_id).all()
                    # print("Number of times(%s,%s): %s" %( sample["resourceId"], minimum_time_node.nodegroup_id, len(related_tiles)))
                    for related_tile in related_tiles:
                        custom_values.add(CustomSearchValue.concept_dt.get_display_value(related_tile, sample_nodes[fsa.MINIMUM_TIME]))
                        custom_values.add(CustomSearchValue.concept_dt.get_display_value(related_tile, sample_nodes[fsa.MAXIMUM_TIME]))

        elif resourceinstance.graph.slug == GraphSlugs.FOSSIL_SAMPLE:
            custom_values.update(CustomSearchValue.get_fossil_types(resourceinstance))

        elif resourceinstance.graph.slug == GraphSlugs.FOSSIL_TYPE:
            # Need to add parent if it is a species
            custom_values.add(resourceinstance.get_descriptor(descriptor="name", context={}))

        elif resourceinstance.graph.slug == GraphSlugs.PUBLICATION:
            # Need to add parent if it is a volume
            custom_values.add(resourceinstance.get_descriptor(descriptor="name", context={}))

        # print("Adding custom values: %s" % custom_values)
        if CustomSearchValue.custom_search_path not in document:
            document[CustomSearchValue.custom_search_path] = []

        for custom_value in custom_values:
            if custom_value:
                # print("Related node value: %s" % custom_value)
                document[CustomSearchValue.custom_search_path].append({"custom_value": custom_value})

    @staticmethod
    def get_parent_fossil_type(fossil_type):
        import arches.app.models.tile as tile

        custom_values = set(())
        print("name: %s" % fossil_type.get_descriptor("name", context={}))
        type_nodes = CustomSearchValue.fossil_type_nodes
        related_tiles = tile.Tile.objects.filter(resourceinstance_id=fossil_type.resourceinstanceid,
                                                 nodegroup__nodegroupid=type_nodes[FossilType.PARENT_NAME].nodegroup_id).all()
        for related_tile in related_tiles:
            custom_values.add(CustomSearchValue.resource_dt.get_display_value(related_tile, type_nodes[FossilType.PARENT_NAME]))

        return custom_values

    @staticmethod
    def get_fossil_types(sample):
        import arches.app.models.tile as tile
        sample_nodes = CustomSearchValue.sample_nodes
        custom_values = set(())
        # print("Sample: %s" % type(sample))
        sample_id = sample["resourceId"] if type(sample) == dict else sample.resourceinstanceid
        related_tiles = tile.Tile.objects.filter(resourceinstance_id=sample_id,
                                                 nodegroup__nodegroupid=sample_nodes[fsa.SCIENTIFIC_NAME].nodegroup_id).all()
        # print("Related tile: %s" % sample)
        for related_tile in related_tiles:
            sci_name_val = CustomSearchValue.resource_dt.get_display_value(related_tile, sample_nodes[fsa.SCIENTIFIC_NAME])
            conn_val = CustomSearchValue.concept_dt.get_display_value(related_tile, sample_nodes[fsa.NAME_CONNECTOR])
            other_name_val = CustomSearchValue.resource_dt.get_display_value(related_tile, sample_nodes[fsa.OTHER_SCIENTIFIC_NAME])
            name_val = ScientificTermsFormatter.format_scientific_name(sci_name_val, conn_val, other_name_val)
            common_val = CustomSearchValue.resource_dt.get_display_value(related_tile, sample_nodes[fsa.FOSSIL_COMMON_NAME])
            custom_values.add(name_val)
            custom_values.add(common_val)

        #print("Returning: %s" % custom_values)
        return custom_values


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
