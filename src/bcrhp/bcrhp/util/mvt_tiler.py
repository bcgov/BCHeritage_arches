from bcgov_arches_common.util.mvt_tiler_common import MVTTiler as MVTTiler_Base


class MVTTiler(MVTTiler_Base):

    def __init__(self):
        pass

    query_cache = {}

    @staticmethod
    def get_query_config():
        return {
            "1b6235b0-0d0f-11ed-98c2-5254008afee6": [
                "authorities",
                "borden_number",
            ],  # Heritage Site
        }
