from django.db import models


class CrhpExportData(models.Model):
    resourceinstanceid = models.UUIDField(primary_key=True)
    site_descriptors = models.JSONField()
    site_names = models.JSONField()
    borden_number = models.CharField()
    sos = models.JSONField()
    addresses = models.JSONField()
    site_boundary = models.IntegerField()
    boundary_geojson = models.CharField()
    site_centroid_latitude = models.FloatField()
    site_centroid_longitude = models.FloatField()
    area_sqm = models.DecimalField(max_digits=12, decimal_places=5)
    heritage_categories = models.JSONField()
    heritage_functions = models.JSONField()
    significant_events = models.JSONField()
    construction_actors = models.JSONField()
    heritage_themes = models.JSONField()
    registration_status = models.CharField()
    registry_types = models.JSONField()
    officially_recognized_site = models.BooleanField()
    protection_events = models.JSONField()
    site_images = models.JSONField()
    external_urls = models.JSONField()

    class Meta:
        managed = False
        db_table = "bcrhp_crhp_data_vw"
