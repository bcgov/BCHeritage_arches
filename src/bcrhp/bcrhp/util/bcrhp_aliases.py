# Classes to standardize the resource model node aliases
class AbstractAliases:
    @staticmethod
    def get_dict(cls):
        newdict = {k: v for k, v in cls.__dict__.items() if not k.startswith('_') and not k == "get_aliases"}
        return newdict


class BCRHPSiteAliases(AbstractAliases):
    BORDEN_NUMBER = 'borden_number'

    NAME = 'name'
    NAME_TYPE = 'name_type'

    EVENT_DATES_APPROXIMATE = 'dates_approximate'
    START_YEAR = 'start_year'
    SIGNIFICANT_EVENTS = 'chronology'

    STREET_NUMBER = 'street_number'
    STREET_NAME = 'street_name'
    CITY = 'city'
    PROVINCE = 'province'
    POSTAL_CODE = 'postal_code'

    RECOGNITION_TYPE = 'recognition_type'
    REGISTRATION_STATUS = 'registration_status'

    SITE_GEOMETRY = 'site_boundary'
    OFFICIALLY_RECOGNIZED = 'officially_recognized_site'

    LEGISLATIVE_ACT = 'legislative_act'

    @staticmethod
    def get_aliases():
        return AbstractAliases.get_dict(BCRHPSiteAliases)


class BCRHPSiteSubmissionAliases(AbstractAliases):
    SUBMITTING_GOVERNMENT = 'submitting_government'
    SUBMISSION_DATE = 'submission_date'
    SUBMITTED_SITE_COUNT = 'total_number_submitted'
    HERITAGE_SITE = 'heritage_site'
    ASSIGNED_TO = 'assigned_to'
    COMPLETION_DATE = 'completion_date'

    @staticmethod
    def get_aliases():
        return AbstractAliases.get_dict(BCRHPSiteSubmissionAliases)

class BCRHPLocalGovernmentAliases:
    TEST = 'test'


class LegislativeActAliases(AbstractAliases):
    ACT_SECTION = 'act_section'
    ACT_STATUS = 'act_status'
    ACTIVE = 'active'
    AUTHORITY = 'authority'
    CITATION = 'citation'
    DOCUMENT = 'document'
    END_DATE = 'end_date'
    LEGAL_INSTRUMENT = 'legal_instrument'
    RECOGNITION_TYPE = 'recognition_type'
    REPLACED_BY = 'replaced_by'
    START_DATE = 'start_date'

    @staticmethod
    def get_aliases():
        return AbstractAliases.get_dict(LegislativeActAliases)

class GraphSlugs:
    HERITAGE_SITE = "heritage_site"
    LEGISLATIVE_ACT = "legislative_act"
    SITE_SUBMISSION = "site_submission"
