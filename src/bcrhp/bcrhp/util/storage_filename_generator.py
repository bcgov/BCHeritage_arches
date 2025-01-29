import os
from arches.app.models import models
from arches.app import datatypes

borden_number_node = None
datatype_factory = None
borden_number_datatype = None


def generate_filename(instance, filename):
    # print("Instance: %s (%s)" % (instance, type(instance)))
    # print("File ID: %s (%s)" % (instance.fileid, type(instance.fileid)))
    # print("Tile: %s (%s)" % (instance.tile, type(instance.tile)))
    # print("ResourceInstance: %s (%s)" % (instance.tile.resourceinstance, type(instance.tile.resourceinstance)))
    # print("GraphID: %s (%s)" % (instance.tile.resourceinstance.graph.graphid, type(instance.tile.resourceinstance.graph.graphid)))
    # print("Graph Slug: %s (%s)" % (instance.tile.resourceinstance.graph.slug, type(instance.tile.resourceinstance.graph.graphid)))
    # return os.sep.join(["images",str(instance.tile.resourceinstance.resourceinstanceid), f"%s__%s" % (instance.fileid, filename)])
    if not hasattr(generate_filename, "borden_number_node"):
        generate_filename.borden_number_node = models.Node.objects.filter(
            alias="borden_number"
        ).first()
        # print("Got borden number node: %s" % str(generate_filename.borden_number_node))

    if not hasattr(generate_filename, "borden_number_datatype"):
        generate_filename.borden_number_datatype = (
            datatypes.datatypes.DataTypeFactory().get_instance(
                generate_filename.borden_number_node.datatype
            )
        )
        # print("Got borden number datatype: %s" % str(generate_filename.borden_number_datatype))

    borden_number_tile = models.TileModel.objects.filter(
        resourceinstance=instance.tile.resourceinstance,
        nodegroup=generate_filename.borden_number_node.nodegroup,
    ).first()
    # print("Got borden number tile: %s" % str(borden_number_tile))
    borden_number = None

    paths = []
    if borden_number_tile:
        borden_number = generate_filename.borden_number_datatype.get_display_value(
            borden_number_tile, generate_filename.borden_number_node
        )
        paths = (
            borden_number.split("-")
            if borden_number and "-" in borden_number
            else [str(instance.tile.resourceinstance.resourceinstanceid)]
        )
    else:
        paths.append(str(instance.tile.resourceinstance.resourceinstanceid))

    graph_slug = (
        instance.tile.resourceinstance.graph.slug
        if instance.tile.resourceinstance.graph.slug
        else "system_settings"
    )
    # print("Paths: %s" % str(paths))
    return os.path.join(graph_slug, *paths, filename)
