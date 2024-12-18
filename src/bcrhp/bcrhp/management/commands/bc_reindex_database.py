from bcgov_arches_common.management.commands.bc_reindex_database import (
    Command as BaseCommand,
)


class Command(BaseCommand):

    def get_index_order(self):
        return [
            "local_government",
            "lg_person",
            "legislative_act",
            "heritage_site",
            "project_sandbox",
            "site_submission",
        ]
