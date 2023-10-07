import os
from arches.app.models import models
from arches.app import datatypes

def generate_filename(instance, filename):
    # print("Instance: %s (%s)" % (instance, type(instance)))
    # print("File ID: %s (%s)" % (instance.fileid, type(instance.fileid)))
    # print("ResourceInstance: %s (%s)" % (instance.tile.resourceinstance, type(instance.tile.resourceinstance)))
    # return os.sep.join(["images",str(instance.tile.resourceinstance.resourceinstanceid), f"%s__%s" % (instance.fileid, filename)])

    if instance.tile.resourceinstance.graph.slug == "publication":
        return get_publication_filename(instance, filename)

    paths = [str(instance.tile.resourceinstance.resourceinstanceid)]
    return os.path.join(str(instance.tile.resourceinstance.graph.slug), *paths, filename)

def get_publication_filename(instance, filename):
    paths = []
    if not hasattr(get_publication_filename, 'publication_year_node'):
        get_publication_filename.publication_year_node = models.Node.objects.filter(alias="year_of_publication").first()
        print(get_publication_filename.publication_year_node.config)

    if not hasattr(get_publication_filename, 'publication_type_node'):
        get_publication_filename.publication_type_node = models.Node.objects.filter(alias="publication_type").first()

    if not hasattr(get_publication_filename, 'publication_year_datatype'):
        get_publication_filename.publication_year_datatype = datatypes.datatypes.DataTypeFactory().get_instance(
            get_publication_filename.publication_year_node.datatype)

    if not hasattr(get_publication_filename, 'publication_type_datatype'):
        get_publication_filename.publication_type_datatype = datatypes.datatypes.DataTypeFactory().get_instance(
            get_publication_filename.publication_type_node.datatype)

    publication_tile = models.TileModel.objects.filter(resourceinstance=instance.tile.resourceinstance, nodegroup=get_publication_filename.publication_year_node.nodegroup).first()

    if publication_tile:
        publication_type = get_publication_filename.publication_type_datatype.get_display_value(publication_tile, get_publication_filename.publication_type_node)
        publication_year = get_publication_filename.publication_year_datatype.get_display_value(publication_tile, get_publication_filename.publication_year_node)

        paths.append(publication_type if publication_type else "unclassified")
        paths.append(publication_year if publication_year else "unknown")

    return os.path.join(str(instance.tile.resourceinstance.graph.slug), *paths, filename)
