from arches.app.search.elasticsearch_dsl_builder import (
    Bool,
    Match,
    Nested,
)
from bcfms.util.bcfms_aliases import FossilSampleAliases as fsa, GraphSlugs
from bcfms.util.business_data_proxy import (
    FossilSampleDataProxy,
    CollectionEventDataProxy,
)
from arches.app.search.es_mapping_modifier import  EsMappingModifier


class CustomSearchValue(EsMappingModifier):
    # custom_search_path = "custom_values"
    initialized = False
    fossil_sample_proxy = None
    collection_event_proxy = None

    # def __init__(self):
    #     pass

    @staticmethod
    def initialize():
        if not CustomSearchValue.initialized:
            CustomSearchValue.fossil_sample_proxy = FossilSampleDataProxy()
            CustomSearchValue.collection_event_proxy = CollectionEventDataProxy()
            CustomSearchValue.initialized = True

    @staticmethod
    def add_search_terms(resourceinstance, document, terms):
        CustomSearchValue.initialize()
        custom_values = set(())

        if resourceinstance.graph.slug == GraphSlugs.COLLECTION_EVENT:
            sample_ids = CustomSearchValue.collection_event_proxy.get_sample_ids(
                resourceinstance
            )

            custom_values |= set(
                CustomSearchValue.fossil_sample_proxy.get_scientific_names_from_samples(
                    sample_ids
                )
            )
            custom_values |= set(
                CustomSearchValue.fossil_sample_proxy.get_common_names_from_samples(
                    sample_ids
                )
            )

            custom_value_aliases = [
                (fsa.MINIMUM_TIME, fsa.MINIMUM_TIME_UNCERTAIN),
                (fsa.MAXIMUM_TIME, fsa.MAXIMUM_TIME_UNCERTAIN),
                (fsa.GEOLOGICAL_GROUP, fsa.GEOLOGICAL_GROUP_UNCERTAIN),
                (fsa.GEOLOGICAL_FORMATION, fsa.GEOLOGICAL_FORMATION_UNCERTAIN),
                (fsa.GEOLOGICAL_MEMBER, fsa.GEOLOGICAL_MEMBER_UNCERTAIN),
                (fsa.FOSSIL_ABUNDANCE, None),
                (fsa.FOSSIL_SIZE_CATEGORY, None),
                (fsa.FOSSIL_SAMPLE_SIGNIFICANT, None),
                (fsa.STORAGE_REFERENCE, None),
            ]
            for alias in custom_value_aliases:
                custom_values |= set(
                    CustomSearchValue.fossil_sample_proxy.get_values_from_samples(
                        samples=sample_ids,
                        node_alias=alias[0],
                        uncertainty_alias=alias[1],
                        flatten=True,
                    )
                )

        elif resourceinstance.graph.slug == GraphSlugs.FOSSIL_SAMPLE:
            custom_values |= set(
                CustomSearchValue.fossil_sample_proxy.get_scientific_names_from_samples(
                    [resourceinstance]
                )
            )
            custom_values |= set(
                CustomSearchValue.fossil_sample_proxy.get_common_names_from_samples(
                    [resourceinstance]
                )
            )
            # custom_values.update(CustomSearchValue.get_fossil_types(resourceinstance))

        elif resourceinstance.graph.slug == GraphSlugs.FOSSIL_TYPE:
            # Need to add parent if it is a species
            custom_values.add(
                resourceinstance.get_descriptor(descriptor="name", context={})
            )

        elif resourceinstance.graph.slug == GraphSlugs.PUBLICATION:
            # Need to add parent if it is a volume
            custom_values.add(
                resourceinstance.get_descriptor(descriptor="name", context={})
            )

        # print("Adding custom values: %s" % custom_values)
        if CustomSearchValue.custom_search_path not in document:
            document[CustomSearchValue.custom_search_path] = []

        for custom_value in custom_values:
            if custom_value:
                document[CustomSearchValue.custom_search_path].append(
                    {"custom_value": custom_value}
                )

    @staticmethod
    def create_nested_custom_filter(term, original_element):
        if "nested" not in original_element:
            return original_element
        # print("Original element: %s" % original_element)
        document_key = CustomSearchValue.custom_search_path
        custom_filter = Bool()
        custom_filter.should(
            Match(
                field="%s.custom_value" % document_key,
                query=term["value"],
                type="phrase_prefix",
            )
        )
        custom_filter.should(
            Match(
                field="%s.custom_value.folded" % document_key,
                query=term["value"],
                type="phrase_prefix",
            )
        )
        nested_custom_filter = Nested(path=document_key, query=custom_filter)
        new_must_element = Bool()
        new_must_element.should(original_element)
        new_must_element.should(nested_custom_filter)
        new_must_element.dsl["bool"]["minimum_should_match"] = 1
        return new_must_element

    @staticmethod
    def add_search_filter(search_query, term):
        # print("Search query before: %s" % search_query)
        original_must_filter = search_query.dsl["bool"]["must"]
        search_query.dsl["bool"]["must"] = []
        for must_element in original_must_filter:
            search_query.must(
                CustomSearchValue.create_nested_custom_filter(term, must_element)
            )

        original_must_filter = search_query.dsl["bool"]["must_not"]
        search_query.dsl["bool"]["must_not"] = []
        for must_element in original_must_filter:
            search_query.must_not(
                CustomSearchValue.create_nested_custom_filter(term, must_element)
            )
        # print("Search query after: %s" % search_query)

    @staticmethod
    def get_mapping_definition():
        return {
            "type": "nested",
            "properties": {
                "custom_value": {
                    "type": "text",
                    "fields": {
                        "raw": {"type": "keyword", "ignore_above": 256},
                        "folded": {"type": "text", "analyzer": "folding"},
                    },
                }
            },
        }
