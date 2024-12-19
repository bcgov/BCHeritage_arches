from arches.app.search.components.base import BaseSearchFilter
from arches.app.search.elasticsearch_dsl_builder import Bool, Terms

details = {
    "searchcomponentid": "",
    "name": "Own Data Filter",
    "icon": "",
    "modulename": "own_data_filter.py",
    "classname": "OwnDataFilter",
    # popup shows icon on RHS of search header, "filter" shows as a tab, "" doesn't show
    "type": "",
    "componentpath": "views/components/search/own-data-filter",
    "componentname": "own-data-filter",
    "sortorder": "0",
    "enabled": True,
}


class OwnDataFilter(BaseSearchFilter):
    def user_in_group(self, group_name):
        return self.request.user.groups.filter(name=group_name).exists()
        # for group in self.request.user.groups.all():
        #     if group_name == group.name:
        #         return True
        # return False

    def append_dsl(
        self, search_results_object, permitted_nodegroups, include_provisional
    ):
        search_query = Bool()
        if self.user_in_group("Local Government"):
            print("\tUser in Local Government... filter")
        else:
            print("\tNo Local Government Filter applied")

        # if include_provisional is not True:
        #     provisional_resource_filter = Bool()
        #
        #     if include_provisional is False:
        #         provisional_resource_filter.filter(Terms(field="provisional_resource", terms=["false", "partial"]))
        #
        #     elif include_provisional == "only provisional":
        #         provisional_resource_filter.filter(Terms(field="provisional_resource", terms=["true", "partial"]))
        #
        #     search_query.must(provisional_resource_filter)
        #     search_results_object["query"].add_query(search_query)
