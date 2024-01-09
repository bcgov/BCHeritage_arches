# Class to standardize the resource model node aliases
class BCRHPSiteAliases:
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

    SITE_GEOMETRY = 'site_boundary'
    OFFICIALLY_RECOGNIZED = 'officially_recognized_site'


class BCRHPSiteSubmissionAliases:
    SUBMITTING_GOVERNMENT = 'submitting_government'
    SUBMISSION_DATE = 'submission_date'
    SUBMITTED_SITE_COUNT = 'total_number_submitted'
    HERITAGE_SITE = 'heritage_site'
    ASSIGNED_TO = 'assigned_to'
    COMPLETION_DATE = 'completion_date'


class BCRHPLocalGovernmentAliases:
    TEST = 'test'

class GraphSlugs:
    HERITAGE_SITE = "heritage_site"