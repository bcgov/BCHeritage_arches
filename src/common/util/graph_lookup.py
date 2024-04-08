from arches.app.models import models
from arches.app.datatypes.datatypes import DataTypeFactory


class GraphLookup:
    _datatype_factory = None
    _datatypes = {}
    _nodes = {}
    _graph_slug = None
    _node_aliases = None

    def __init__(self, graph_slug, node_aliases):
        self._graph_slug = graph_slug
        self._node_aliases = node_aliases.values() if isinstance(node_aliases, dict) else node_aliases

    def initialize(self):
        # This needs to be deferred to ensure the database is created when being redeployed otherwise the graph
        # tries to initialize before the database is setup
        if not self._datatype_factory:
            self._datatype_factory = DataTypeFactory()
            for alias in self._node_aliases:
                node = models.Node.objects.filter(
                    alias=alias,
                    graph__slug=self._graph_slug
                ).first()
                if node:
                    self._nodes[alias] = node
                    self._datatypes[alias] = self._datatype_factory.get_instance(node.datatype)

    def get_node(self, node_alias):
        self.initialize()
        if node_alias not in self._nodes:
            raise KeyError("Graph %s not configured for node %s" % (self._graph_slug, node_alias))
        return self._nodes[node_alias]

    def get_datatype(self, node_alias):
        self.initialize()
        if node_alias not in self._nodes:
            raise KeyError("Graph %s not configured for node %s" % (self._graph_slug, node_alias))
        return self._datatypes[node_alias]
