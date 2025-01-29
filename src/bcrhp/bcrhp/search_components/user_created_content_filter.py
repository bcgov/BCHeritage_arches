from arches.app.utils.betterJSONSerializer import JSONDeserializer
from arches.app.search.elasticsearch_dsl_builder import Bool, Terms
from arches.app.search.components.base import BaseSearchFilter

details = {
    "searchcomponentid": "",
    "name": "User Created Content Filter",
    "icon": "",
    "modulename": "user_created_content_filter.py",
    "classname": "UserCreatedContentFilter",
    "type": "filter",
    "componentpath": "",
    "componentname": "",
    "sortorder": "0",
    "enabled": True,
}


class UserCreatedContentFilter(BaseSearchFilter):
    def append_dsl(
        self, search_results_object, permitted_nodegroups, include_provisional
    ):
        search_query = Bool()
        querystring_params = self.request.GET.get(details["componentname"], "")

        graph_ids = []
        for resourceTypeFilter in JSONDeserializer().deserialize(querystring_params):
            graph_ids.append(str(resourceTypeFilter["graphid"]))

        terms = Terms(field="graph_id", terms=graph_ids)
        if resourceTypeFilter["inverted"] is True:
            search_query.must_not(terms)
        else:
            search_query.filter(terms)

        search_results_object["query"].add_query(search_query)
