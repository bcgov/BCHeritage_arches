import os
def generate_filename(instance, filename):
    # print("Instance: %s (%s)" % (instance, type(instance)))
    # print("File ID: %s (%s)" % (instance.fileid, type(instance.fileid)))
    # print("Tile: %s (%s)" % (instance.tile, type(instance.tile)))
    # print("ResourceInstance: %s (%s)" % (instance.tile.resourceinstance, type(instance.tile.resourceinstance)))
    # return os.sep.join(["images",str(instance.tile.resourceinstance.resourceinstanceid), f"%s__%s" % (instance.fileid, filename)])
    paths = [str(instance.tile.resourceinstance.resourceinstanceid)]
    return os.sep.join([str(instance.tile.resourceinstance.graph.slug), *paths, str(instance.tile.resourceinstance.resourceinstanceid), filename])
