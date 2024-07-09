# Classes to standardize the resource model node aliases
class AbstractAliases:
    @staticmethod
    def get_dict(cls):
        newdict = {
            k: v
            for k, v in cls.__dict__.items()
            if not k.startswith("_") and not k == "get_aliases"
        }
        return newdict


class BCRHPSiteAliases(AbstractAliases):

    ACCURACY_REMARKS = "accuracy_remarks"
    BCRHP_SUBMISSION_STATUS = "bcrhp_submission_status"
    BORDEN_NUMBER = "borden_number"
    CHILD_SITES = "child_sites"
    CHRONOLOGY = "chronology"
    CHRONOLOGY_NOTES = "chronology_notes"
    CITY = "city"
    CONSTRUCTION_ACTOR = "construction_actor"
    CONSTRUCTION_ACTOR_NOTES = "construction_actor_notes"
    CONSTRUCTION_ACTOR_TYPE = "construction_actor_type"
    CONTRIBUTING_RESOURCE_COUNT = "contributing_resource_count"
    COPYRIGHT = "copyright"
    CRHP_SUBMISSION_STATUS = "crhp_submission_status"
    DATES_APPROXIMATE = "dates_approximate"
    DATE_SUBMITTED_TO_CRHP = "date_submitted_to_crhp"
    DEFINING_ELEMENTS = "defining_elements"
    DESIGNATION_OR_PROTECTION_END_DATE = "designation_or_protection_end_date"
    DESIGNATION_OR_PROTECTION_START_DATE = "designation_or_protection_start_date"
    DOCUMENT_DESCRIPTION = "document_description"
    DOCUMENT_LOCATION = "document_location"
    DOCUMENT_TYPE = "document_type"
    END_YEAR = "end_year"
    EXTERNAL_URL = "external_url"
    EXTERNAL_URL_TYPE = "external_url_type"
    FEDERAL_ID_NUMBER = "federal_id_number"
    FUNCTIONAL_CATEGORY = "functional_category"
    FUNCTIONAL_STATE = "functional_state"
    HERITAGE_CATEGORY = "heritage_category"
    HERITAGE_THEME = "heritage_theme"
    HERITAGE_VALUE = "heritage_value"
    IMAGE_DATE = "image_date"
    IMAGE_DESCRIPTION = "image_description"
    IMAGE_FEATURES = "image_features"
    IMAGE_TYPE = "image_type"
    IMAGE_VIEW = "image_view"
    INFORMATION_SOURCE = "information_source"
    INTERNAL_REMARK = "internal_remark"
    LEGAL_ADDRESS_INTERNAL_NOTES = "legal_address_internal_notes"
    LEGAL_DESCRIPTION = "legal_description"
    LEGISLATIVE_ACT = "legislative_act"
    LOCALITY = "locality"
    LOCATION_DESCRIPTION = "location_description"
    NAME = "name"
    NAME_TYPE = "name_type"
    OFFICIALLY_RECOGNIZED_SITE = "officially_recognized_site"
    OWNERSHIP = "ownership"
    PHOTOGRAPHER = "photographer"
    PHYSICAL_DESCRIPTION = "physical_description"
    PID = "pid"
    PIN = "pin"
    POSTAL_CODE = "postal_code"
    PRIMARY_IMAGE = "primary_image"
    PROTECTION_NOTES = "protection_notes"
    PROVINCE = "province"
    REFERENCE_NUMBER = "reference_number"
    REGISTRATION_STATUS = "registration_status"
    REGISTRY_TYPES = "registry_types"
    REMARK_DATE = "remark_date"
    REMARK_TYPE = "remark_type"
    RESPONSIBLE_GOVERNMENT = "responsible_government"
    RESTRICTED = "restricted"
    SIGNIFICANCE_TYPE = "significance_type"
    SITE_BOUNDARY = "site_boundary"
    SITE_DOCUMENT = "site_document"
    SITE_IMAGES = "site_images"
    SOURCE_NOTES = "source_notes"
    START_YEAR = "start_year"
    STREET_ADDRESS = "street_address"
    SUBMIT_TO_CRHP = "submit_to_crhp"

    @staticmethod
    def get_aliases():
        return AbstractAliases.get_dict(BCRHPSiteAliases)


class BCRHPSiteSubmissionAliases(AbstractAliases):
    SUBMITTING_GOVERNMENT = "submitting_government"
    SUBMISSION_DATE = "submission_date"
    SUBMITTED_SITE_COUNT = "total_number_submitted"
    HERITAGE_SITE = "heritage_site"
    ASSIGNED_TO = "assigned_to"
    COMPLETION_DATE = "completion_date"

    @staticmethod
    def get_aliases():
        return AbstractAliases.get_dict(BCRHPSiteSubmissionAliases)


class BCRHPLocalGovernmentAliases:
    TEST = "test"


class LegislativeActAliases(AbstractAliases):
    ACT_SECTION = "act_section"
    ACT_STATUS = "act_status"
    ACTIVE = "active"
    AUTHORITY = "authority"
    CITATION = "citation"
    DOCUMENT = "document"
    END_DATE = "end_date"
    LEGAL_INSTRUMENT = "legal_instrument"
    RECOGNITION_TYPE = "recognition_type"
    REPLACED_BY = "replaced_by"
    START_DATE = "start_date"

    @staticmethod
    def get_aliases():
        return AbstractAliases.get_dict(LegislativeActAliases)


class GraphSlugs:
    HERITAGE_SITE = "heritage_site"
    LEGISLATIVE_ACT = "legislative_act"
    SITE_SUBMISSION = "site_submission"
