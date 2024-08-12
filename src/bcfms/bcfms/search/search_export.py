from arches.app.search.search_export import SearchResultsExporter
from django.db import connection


class BCFMSSearchResultsExporter(SearchResultsExporter):
    def __init__(self, search_request=None):
        super().__init__(search_request)

    def refresh_materialized_views(self, cursor):
        cursor.execute("refresh materialized view fossil_collection_event.collection_event_location_mv")
        cursor.execute("refresh materialized view fossil_collection_event.samples_collected_mv")

    def to_csv(self, instances, headers, name):
        if name == "Fossil Collection Event":
            collection_ids = [o['resourceid'] for o in instances]
            with connection.cursor() as cur:
                # self.refresh_materialized_views(cur)
                cur.execute("""select * from fossil_collection_event.collection_event_csv_export_vw where array_position(%s, collection_event_id::text) is not null""", [collection_ids])
                columns = [desc[0] for desc in cur.description]
                return super().to_csv([dict(zip(columns, row)) for row in cur.fetchall()], columns, name)
        return super().to_csv(instances, headers, name)
