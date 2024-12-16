from bcgov_arches_common.util.mvt_tiler_common import MVTTiler as MVTTiler_Base

class MVTTiler(MVTTiler_Base):

    def __init__(self):
        pass

    query_cache = {}

    @staticmethod
    def get_query_config():
        return {'5bfa1354-b6e1-11ee-9438-080027b7463b': ['size_categories'],  # collection_event, collection_location
                'c66518e2-10c6-11ec-adef-5254008afee6': ['name', 'ranking'],
                'dd19c7c6-0202-11ed-a511-0050568377a0': ['name', 'ranking'],  # protected_site, area_boundary
                '2336968c-1035-11ec-a3aa-5254008afee6': ['name', 'ranking'],  # fossil_site, area_boundary
                '4fe7beb2-1f3a-11ed-a99d-5254008afee6': ['name', 'ranking'],
                }
