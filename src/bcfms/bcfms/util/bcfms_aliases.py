# Class to standardize the resource model node aliases
class AbstractAliases:
    @staticmethod
    def get_dict(cls):
        newdict = {k: v for k, v in cls.__dict__.items() if not k.startswith('_') and not k == "get_aliases"}
        return newdict


class CollectionEventAliases(AbstractAliases):
    START_YEAR = 'collection_start_year'
    LOCATION_DESCRIPTOR = 'location_descriptor'
    NTS_MAPSHEET_NAME = 'nts_mapsheet_name'

    DETAILED_LOCATION = 'detailed_location'
    SAMPLES_COLLECTED = 'samples_collected'

    @staticmethod
    def get_aliases():
        return AbstractAliases.get_dict(CollectionEventAliases)


class FossilSampleAliases(AbstractAliases):
    FORMATION = 'geological_formation'
    FORMATION_UNCERTAIN = 'geological_formation_uncertain'

    SCIENTIFIC_NAME = 'scientific_name'
    NAME_CONNECTOR = 'open_nomanclature_term'
    OTHER_SCIENTIFIC_NAME = 'other_scientific_name'
    FOSSIL_COMMON_NAME = 'fossil_common_name'
    COMMON_NAME_UNCERTAIN = 'common_name_uncertain'

    MINIMUM_TIME = 'minimum_time'
    MINIMUM_TIME_UNCERTAIN = 'minimum_time_uncertain'

    @staticmethod
    def get_aliases():
        return AbstractAliases.get_dict(FossilSampleAliases)


class PublicationAliases(AbstractAliases):
    TITLE = 'title'
    AUTHORS = 'authors'
    NAME_TYPE = 'name_type'
    PUBLICATION_YEAR = 'year_of_publication'
    PUBLICATION_TYPE = 'publication_type'
    JOURNAL_OR_PUBLICATION_NAME = 'journal_or_volume_name'

    @staticmethod
    def get_aliases():
        return AbstractAliases.get_dict(PublicationAliases)


class FossilType(AbstractAliases):
    NAME = 'name'
    NAME_TYPE = 'name_type'
    PARENT_NAME = 'parent_name'
    TAXONOMIC_RANK = 'taxonomic_rank'
    SIZE_CATEGORY = 'size_category'

    @staticmethod
    def get_aliases():
        return AbstractAliases.get_dict(FossilType)

class GraphSlugs:
    COLLECTION_EVENT = 'collection_event'
    CONTRIBUTOR = 'contributor'
    FOSSIL_SAMPLE = 'fossil_sample'
    FOSSIL_SITE = 'fossil_site'
    FOSSIL_TYPE = 'fossil_type'
    IMPORTANT_AREA = 'important_area'
    PROJECT_ASSESSMENT = 'project_assessment'
    PROJECT_SANDBOX = 'project_sandbox'
    PROTECTED_SITE = 'protected_site'
    PUBLICATION = 'publication'
    REPORTED_FOSSIL = 'reported_fossil'
    RESEARCH_PERMIT = 'research_permit'
    STORAGE_LOCATION = 'storage_location'

if __name__ == '__main__':
    print(FossilSampleAliases.get_aliases()[FossilSampleAliases.FOSSIL_COMMON_NAME])
