# Class to standardize the resource model node aliases
class AbstractAliases:
    @staticmethod
    def get_dict(cls):
        newdict = {
            k: v
            for k, v in cls.__dict__.items()
            if not k.startswith("_") and not k == "get_aliases"
        }
        return newdict


class CollectionEventAliases(AbstractAliases):
    START_YEAR = "collection_start_year"
    LOCATION_DESCRIPTOR = "location_descriptor"
    NTS_MAPSHEET_NAME = "nts_mapsheet_name"

    DETAILED_LOCATION = "detailed_location"
    SAMPLES_COLLECTED = "samples_collected"

    @staticmethod
    def get_aliases():
        return AbstractAliases.get_dict(CollectionEventAliases)


class FossilSampleAliases(AbstractAliases):
    GEOLOGICAL_GROUP = "geological_group"
    GEOLOGICAL_GROUP_UNCERTAIN = "geological_group_uncertain"

    GEOLOGICAL_FORMATION = "geological_formation"
    GEOLOGICAL_FORMATION_UNCERTAIN = "geological_formation_uncertain"

    GEOLOGICAL_MEMBER = "geological_member"
    GEOLOGICAL_MEMBER_UNCERTAIN = "geological_member_uncertain"

    SCIENTIFIC_NAME = "scientific_name"
    NAME_CONNECTOR = "open_nomanclature_term"
    OTHER_SCIENTIFIC_NAME = "other_scientific_name"
    FOSSIL_COMMON_NAME = "fossil_common_name"
    COMMON_NAME_UNCERTAIN = "common_name_uncertain"

    MINIMUM_TIME = "minimum_time"
    MINIMUM_TIME_UNCERTAIN = "minimum_time_uncertain"
    MAXIMUM_TIME = "maximum_time"
    MAXIMUM_TIME_UNCERTAIN = "maximum_time_uncertain"

    FOSSIL_ABUNDANCE = "fossil_abundance"
    FOSSIL_SIZE_CATEGORY = "fossil_size_category_v"
    FOSSIL_SAMPLE_SIGNIFICANT = "fossil_sample_significant"

    STORAGE_REFERENCE = "storage_reference"

    @staticmethod
    def get_aliases():
        return AbstractAliases.get_dict(FossilSampleAliases)


class PublicationAliases(AbstractAliases):
    TITLE = "title"
    AUTHORS = "authors"
    NAME_TYPE = "name_type"
    PUBLICATION_YEAR = "year_of_publication"
    PUBLICATION_TYPE = "publication_type"
    JOURNAL_OR_PUBLICATION_NAME = "journal_or_volume_name"

    @staticmethod
    def get_aliases():
        return AbstractAliases.get_dict(PublicationAliases)


class FossilType(AbstractAliases):
    NAME = "name"
    NAME_TYPE = "name_type"
    PARENT_NAME = "parent_name"
    TAXONOMIC_RANK = "taxonomic_rank"
    SIZE_CATEGORY = "size_category"

    @staticmethod
    def get_aliases():
        return AbstractAliases.get_dict(FossilType)


class IPA(AbstractAliases):
    ASSESSMENT_COMPLETION_DATE = "assessment_completion_date"
    ASSESSMENT_CRITERIA = "assessment_criteria"
    ASSESSMENT_START_DATE = "assessment_start_date"
    CFP_APPROVAL_DATE = "cfp_approval_date"
    CFP_APPROVAL_STATUS = "cfp_approval_status"
    CFP_DOCUMENT = "cfp_document"
    CFP_INTERNAL_NOTES = "cfp_internal_notes"
    CFP_NUMBER = "cfp_number"
    CFP_PALEO_COMPANY = "cfp_paleo_company"
    CFP_PALEO_CONSULTANT = "cfp_paleo_consultant"
    CFP_REPORT = "cfp_report"
    CFP_RESPONSE = "cfp_response"
    CFP_TITLE = "cfp_title"
    CHANCE_FIND_PROTOCOL = "chance_find_protocol"
    COLLECTION_EVENTS = "collection_events"
    COMMUNICATION_DATE = "communication_date"
    COMMUNICATION_NOTE = "communication_note"
    COMMUNICATIONS_LOG = "communications_log"
    EXTERNAL_CONTACT = "external_contact"
    FIA_CONSULTANT_REPORT_NUMBER_N1 = "fia_consultant_report_number_n1"
    FIA_FILE = "fia_file"
    FIA_FMO_APPROVAL_STATUS = "fia_fmo_approval_status"
    FIA_FMO_ASSESSMENT = "fia_fmo_assessment"
    FIA_FMO_DETERMINED_LEVEL_OF_RISK = "fia_fmo_determined_level_of_risk"
    FIA_FMO_INTERNAL_NOTES = "fia_fmo_internal_notes"
    FIA_FMO_RESPONSE = "fia_fmo_response"
    FIA_FOSSIL_REPOSITORY_AGREEMENT = "fia_fossil_repository_agreement"
    FIA_PALEO_COMPANY = "fia_paleo_company"
    FIA_PALEO_CONSULTANT = "fia_paleo_consultant"
    FIAP_CONSULTANT_REPORT_NUMBER = "fiap_consultant_report_number"
    FIAP_FILE = "fiap_file"
    FIAP_FMO_APPROVAL_STATUS = "fiap_fmo_approval_status"
    FIAP_FMO_ASSESSMENT = "fiap_fmo_assessment"
    FIAP_FMO_INTERNAL_NOTES = "fiap_fmo_internal_notes"
    FIAP_FMO_RESPONSE = "fiap_fmo_response"
    FIAP_PALEO_COMPANY = "fiap_paleo_company"
    FIAP_PALEO_CONSULTANT = "fiap_paleo_consultant"
    FIAP_REPORT = "fiap_report"
    FIAP_REPORT_NUMBER = "fiap_report_number"
    FIAP_REPORT_RECOMMENDATION = "fiap_report_recommendation"
    FIAP_REPORT_TITLE = "fiap_report_title"
    FIA_REPORT = "fia_report"
    FIA_REPORT_NUMBER = "fia_report_number"
    FIA_REPORT_RECOMMENDATIONS = "fia_report_recommendations"
    FIA_REPORT_TITLE = "fia_report_title"
    FMO_ACTOR = "fmo_actor"
    FOSSIL_IMPACT_ASSESSMENT = "fossil_impact_assessment"
    FOSSIL_IMPACT_ASSESSMENT_PLAN = "fossil_impact_assessment_plan"
    FOSSIL_IMPACT_ASSESSMENT_PROCESS = "fossil_impact_assessment_process"
    FRPR = "frpr"
    GEOMETRY_QUALIFIER = "geometry_qualifier"
    GROUND_DISTURBANCE = "ground_disturbance"
    IGNEOUS_ROCK = "igneous_rock"
    IMPACT_MITIGATION_PLAN = "impact_mitigation_plan"
    IMPACT_MITIGATION_PROCESS = "impact_mitigation_process"
    IMP_CONSULTANT_REPORT_NUMBER = "imp_consultant_report_number"
    IMP_FMO_APPROVAL_STATUS = "imp_fmo_approval_status"
    IMP_FMO_ASSESSMENT = "imp_fmo_assessment"
    IMP_FMO_INTERNAL_NOTES = "imp_fmo_internal_notes"
    IMP_FMO_RESPONSE = "imp_fmo_response"
    IMP_FOSSIL_REPOSITORY_AGREEMENT = "imp_fossil_repository_agreement"
    IMP_PALEO_COMPANY = "imp_paleo_company"
    IMP_PALEO_CONSULTANT = "imp_paleo_consultant"
    IMP_RECOMMENDATIONS = "imp_recommendations"
    IMP_REPORT_NUMBER = "imp_report_number"
    IMP_TITLE = "imp_title"
    INDUSTRY_PROJECT_ASSESSMENT = "industry_project_assessment"
    INITIAL_PROJECT_REVIEW = "initial_project_review"
    INITIAL_REVIEW_INTERNAL_NOTES = "initial_review_internal_notes"
    INITIAL_REVIEW_LEVEL_OF_RISK = "initial_review_level_of_risk"
    INITIAL_REVIEW_OUTCOME = "initial_review_outcome"
    INTERSECTS_IFA = "intersects_ifa"
    IPA_PHASE = "ipa_phase"
    LAND_ACT_FILE_NUMBER = "land_act_file_number"
    LOCATION_DESCRIPTION = "location_description"
    METAMORPHIC_ROCK = "metamorphic_rock"
    MITIGATION_PLAN_FILE = "mitigation_plan_file"
    MULTIPLE_GEOMETRY_QUALIFIER = "multiple_geometry_qualifier"
    OTHER_PROJECT_TYPE = "other_project_type"
    PHOTOGRAPH_DATE = "photograph_date"
    PHOTOGRAPH_DESCRIPTION = "photograph_description"
    PHOTOGRAPHER = "photographer"
    PHOTOGRAPH_VIEW = "photograph_view"
    PRELIMINARY_STUDY_PROCESS = "preliminary_study_process"
    PROJECT_AUTHORIZING_AGENCY = "project_authorizing_agency"
    PROJECT_COMPLETED = "project_completed"
    PROJECT_DETAILS = "project_details"
    PROJECT_DOCUMENTS = "project_documents"
    PROJECT_END_DATE = "project_end_date"
    PROJECT_INITIATOR = "project_initiator"
    PROJECT_LOCATION = "project_location"
    PROJECT_NAME = "project_name"
    PROJECT_SITE = "project_site"
    PROJECT_START_DATE = "project_start_date"
    PROJECT_STATUS = "project_status"
    PROJECT_TYPE = "project_type"
    PROPOSED_ACTIVITY = "proposed_activity"
    PROXIMITY_TO_FOS = "proximity_to_fos"
    PSR_CONSULTANT_REPORT_NUMBER = "psr_consultant_report_number"
    PSR_FILE = "psr_file"
    PSR_FMO_APPROVAL_STATUS = "psr_fmo_approval_status"
    PSR_FMO_ASSESSMENT = "psr_fmo_assessment"
    PSR_FMO_DETERMINED_LEVEL_OF_RISK = "psr_fmo_determined_level_of_risk"
    PSR_FMO_INTERNAL_NOTES = "psr_fmo_internal_notes"
    PSR_FMO_RESPONSE = "psr_fmo_response"
    PSR_NUMBER = "psr_number"
    PSR_PALEO_COMPANY = "psr_paleo_company"
    PSR_PALEO_CONSULTANT = "psr_paleo_consultant"
    PSR_RECOMMENDATION = "psr_recommendation"
    PSR_REPORT = "psr_report"
    PSR_TITLE = "psr_title"
    QUATERNARY_DEPOSITS = "quaternary_deposits"
    RISK_ASSESSMENT = "risk_assessment"
    SAP_CONSULTANT_REPORT_NUMBER = "sap_consultant_report_number"
    SAP_FMO_APPROVAL_STATUS = "sap_fmo_approval_status"
    SAP_FMO_ASSESSMENT = "sap_fmo_assessment"
    SAP_FMO_INTERNAL_NOTES = "sap_fmo_internal_notes"
    SAP_FMO_RESPONSE = "sap_fmo_response"
    SAP_FOSSIL_REPOSITORY_AGREEMENT = "sap_fossil_repository_agreement"
    SAP_PALEO_COMPANY = "sap_paleo_company"
    SAP_PALEO_CONSULTANT = "sap_paleo_consultant"
    SAP_RECOMMENDATIONS = "sap_recommendations"
    SAP_REPORT_NUMBER = "sap_report_number"
    SAP_TITLE = "sap_title"
    SEDIMENTARY_ROCK = "sedimentary_rock"
    SITE_ASSESSMENT_PHOTOGRAPHS = "site_assessment_photographs"
    SITE_ASSESSMENT_PLAN = "site_assessment_plan"
    SITE_ASSESSMENT_PLAN_FILE = "site_assessment_plan_file"
    SITE_ASSESSMENT_PROCESS = "site_assessment_process"

    @staticmethod
    def get_aliases():
        return AbstractAliases.get_dict(IPA)


class GraphSlugs:
    COLLECTION_EVENT = "collection_event"
    CONTRIBUTOR = "contributor"
    FOSSIL_SAMPLE = "fossil_sample"
    FOSSIL_SITE = "fossil_site"
    FOSSIL_TYPE = "fossil_type"
    IMPORTANT_AREA = "important_area"
    PROJECT_ASSESSMENT = "project_assessment"
    PROJECT_SANDBOX = "project_sandbox"
    PROTECTED_SITE = "protected_site"
    PUBLICATION = "publication"
    REPORTED_FOSSIL = "reported_fossil"
    RESEARCH_PERMIT = "research_permit"
    STORAGE_LOCATION = "storage_location"


if __name__ == "__main__":
    print(FossilSampleAliases.get_aliases()[FossilSampleAliases.FOSSIL_COMMON_NAME])
