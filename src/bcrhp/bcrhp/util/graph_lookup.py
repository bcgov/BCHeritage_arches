from arches.app.models import models
from arches.app.datatypes.datatypes import DataTypeFactory


class GraphLookup:
    _datatype_factory = DataTypeFactory()
    _datatypes = {}
    _nodes = {}
    _graph_slug = None

    def __init__(self, graph_slug, node_aliases):
        self._graph_slug = graph_slug
        for alias in node_aliases:
            node = models.Node.objects.filter(
                alias=alias,
                graph__slug=graph_slug
            ).first()
            if node:
                self._nodes[alias] = node
                self._datatypes[alias] = self._datatype_factory.get_instance(node.datatype)

    def get_node(self, node_alias):
        if node_alias not in self._nodes:
            raise KeyError("Graph %s not configured for node %s" % (self._graph_slug, node_alias))
        return self._nodes[node_alias]

    def get_datatype(self, node_alias):
        if node_alias not in self._nodes:
            raise KeyError("Graph %s not configured for node %s" % (self._graph_slug, node_alias))
        return self._datatypes[node_alias]
