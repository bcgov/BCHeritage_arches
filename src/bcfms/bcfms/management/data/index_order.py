def get_index_order():
    # NB - Publication is done twice to handle the recursive relationship for the descriptors
    return [
        "important_area",
        "protected_site",
        "contributor",
        "fossil_site",
        "fossil_type",
        "storage_location",
        "fossil_sample",
        "research_permit",
        "collection_event",
        "project_sandbox",
        "reported_fossil",
        "project_assessment",
        "publication",
        "publication"
    ]