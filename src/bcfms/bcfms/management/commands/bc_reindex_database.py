from bcgov_arches_common.management.commands.bc_reindex_database import (
    Command as BaseCommand,
)


class Command(BaseCommand):

    def get_index_order(self):
        return [
            "important_area",
            "protected_site",
            "contributor",
            "fossil_site",
            "fossil_type",
            "storage_location",
            "fossil_sample",
            "research_permit",
            "collection_event",
            "project_sandbox",
            "reported_fossil",
            "project_assessment",
            "publication",
            "publication",
        ]
