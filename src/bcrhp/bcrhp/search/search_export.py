from arches.app.search.search_export import SearchResultsExporter
from django.db import connection
from arches.app.models import models
from bcrhp.util.bcrhp_aliases import GraphSlugs


class BCRHPSearchResultsExporter(SearchResultsExporter):

    def to_csv(self, instances, headers, name):
        if name == "Heritage Site":
            if self.search_request.user.username == "anonymous":  # Anonymous users use the view
                collection_ids = [o["resourceid"] for o in instances]

                with connection.cursor() as cur:
                    cur.execute(
                        """
                        select *
                        from heritage_site.csv_export
                        where array_position(%s, site_id::text) is not null
                    """,
                        [collection_ids],
                    )
                    columns = [desc[0] for desc in cur.description]
                    results = [dict(zip(columns, row)) for row in cur.fetchall()]
                    return super().to_csv(results, columns, name)
            else:  # We're an authenticated user - show all the nodes
                graph = models.GraphModel.objects.get(slug=GraphSlugs.HERITAGE_SITE)
                headers = self.return_ordered_header(graph.graphid, "csv")
                headers.append("resourceid")
                return super().to_csv(instances, headers, name)

        return super().to_csv(instances, headers, name)
