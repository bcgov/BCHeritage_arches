from arches.app.search.components.term_filter import TermFilter as BaseTermFilter


class TermFilter(BaseTermFilter):


    def append_dsl(self, search_results_object, permitted_nodegroups, include_provisional):
        super(TermFilter, self).append_dsl(search_results_object, permitted_nodegroups, include_provisional)
