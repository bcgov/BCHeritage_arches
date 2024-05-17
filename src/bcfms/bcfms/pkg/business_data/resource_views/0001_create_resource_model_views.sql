select __arches_create_resource_model_views(graphid)
from graphs
where isresource = true
  and publicationid is not null
  and name->>'en' != 'Arches System Settings';