from arches.app.search.search_export import SearchResultsExporter
from django.db import connection

class BCRHPSearchResultsExporter(SearchResultsExporter):

    def to_csv(self, instances, headers, name):
        if name == "Heritage Site":
            collection_ids = [o['resourceid'] for o in instances]

            with connection.cursor() as cur:
                cur.execute("""
                    select *
                    from heritage_site.csv_export
                    where array_position(%s, site_id::text) is not null
                """, [collection_ids])
                columns = [desc[0] for desc in cur.description]
                instance_results = [dict(zip(instance_columns, row)) for row in cur.fetchall()]
                print(instance_results[0])

                return super().to_csv(instance_results, instance_columns, name)

        return super().to_csv(instances, headers, name)

