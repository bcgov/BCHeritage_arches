from arches.app.functions.primary_descriptors import AbstractPrimaryDescriptorsFunction
from arches.app.models import models
from arches.app.datatypes.datatypes import DataTypeFactory
from django.utils.translation import ugettext as _

details = {
    "functionid": "60000000-0000-0000-0000-000000001001",
    "name": "BC Fossils Descriptors",
    "type": "primarydescriptors",
    "modulename": "bc_fossils_descriptors.py",
    "description": "Function that provides the primary descriptors for BC Fossils resources",
    "defaultconfig": {
        "module": "arches_fossils.functions.bc_fossils_descriptors",
        "class_name": "BCFossilsDescriptors",
        "descriptor_types": {
            "name": {
                "type": "name",
                "node_ids": [],
                "first_only": True,
                "show_name": False,
            },
            "description": {
                "type": "description",
                "node_ids": [],
                "first_only": False,
                "delimiter": "<br>",
                "show_name": True,
            },
            "map_popup": {
                "type": "map_popup",
                "node_ids": [],
                "first_only": False,
                "delimiter": "<br>",
                "show_name": True,
            },
        },
        "triggering_nodegroups": [],
    },
    "classname": "BCFossilsDescriptors",
    "component": "views/components/functions/bc-fossils-descriptors",
}


class BCFossilsDescriptors(AbstractPrimaryDescriptorsFunction):
    _sample_graph_name = {"en": "BC Fossil Sample"}
    _datatype_factory = None
    _formation_node = None
    _geologic_minimum_time_node = None
    _collected_fossils_node = None
    _collection_event_graph_id = None
    _coll_event_samples_values_config = None
    _coll_event_popup_order = ["Detailed Location", "Formation", "Period", "Samples Collected"]
    _coll_event_card_order = ["Detailed Location", "Period", "Samples Collected"]

    @staticmethod
    def initialize_static_data():
        BCFossilsDescriptors._formation_node = models.Node.objects.filter(
            alias='geological_formation',
            graph__name__contains=BCFossilsDescriptors._sample_graph_name
        ).first()
        BCFossilsDescriptors._geologic_minimum_time_node = models.Node.objects.filter(
            alias='minimum_time',
            graph__name__contains=BCFossilsDescriptors._sample_graph_name
        ).first()
        BCFossilsDescriptors._collected_fossils_node = models.Node.objects.filter(
            alias="samples_collected",
        ).first()
        BCFossilsDescriptors._collection_event_graph_id = \
        models.GraphModel.objects.filter(
            name__contains={"en": "BC Fossil Collection Event"}
        ).filter(isresource=True).values(
            "graphid").first()["graphid"]
        BCFossilsDescriptors._coll_event_samples_values_config = [
            {"node": BCFossilsDescriptors._formation_node, "label": "Formation"},
            {"node": BCFossilsDescriptors._geologic_minimum_time_node, "label": "Period"}]

    def get_primary_descriptor_from_nodes(self, resource, config, context=None):
        return_value = None
        display_values = {}

        if BCFossilsDescriptors._formation_node is None:
            BCFossilsDescriptors.initialize_static_data()

        try:
            if resource.graph_id == self._collection_event_graph_id and config["type"] == "name":
                return self._get_site_name(resource)

            if resource.graph_id == self._collection_event_graph_id:
                display_values = self._get_sample_values(resource, self._coll_event_samples_values_config)

            name_nodes = models.Node.objects.filter(graph=resource.graph_id).filter(
                nodeid__in=config['node_ids']
            )
            sorted_name_nodes = sorted(name_nodes, key=lambda row: config['node_ids'].index(str(row.nodeid)), reverse=False)

            for name_node in sorted_name_nodes:
                value = self._get_value_from_node(name_node, resource)
                if value:
                    if config["first_only"]:
                        return self._format_value(name_node.name, value, config)
                    display_values[name_node.name] = value

            if resource.graph_id == BCFossilsDescriptors._collection_event_graph_id:
                for label in (
                        BCFossilsDescriptors._coll_event_popup_order if config["type"] == "map_popup" else BCFossilsDescriptors._coll_event_card_order):
                    if label in display_values:
                        if not return_value:
                            return_value = ""
                        else:
                            return_value += config["delimiter"]
                        return_value += self._format_value(label, display_values[label], config)
            else:
                for key in display_values.keys():
                    if not return_value:
                        return_value = ""
                    else:
                        return_value += config["delimiter"]
                    return_value += self._format_value(key, display_values[key], config)

            return return_value
        except ValueError as e:
            print(e, "invalid nodegroupid participating in descriptor function.")

    def _get_value_from_node(self, name_node, resourceinstanceid):

        tile = models.TileModel.objects.filter(
            nodegroup_id=name_node.nodegroup_id
        ).filter(resourceinstance_id=resourceinstanceid).first()
        if not tile:
            return None
        datatype = self._get_datatype_factory().get_instance(name_node.datatype)
        return datatype.get_display_value(tile, name_node)

    def _get_datatype_factory(self):
        if not self._datatype_factory:
            self._datatype_factory = DataTypeFactory()
        return self._datatype_factory

    def _get_sample_values(self, resource, values_config):
        # print("Resource: %s" % resource.resourceinstanceid)
        return_values = {}

        fossil_sample_values = models.ResourceXResource.objects.filter(
            resourceinstanceidfrom=resource.resourceinstanceid,
            nodeid=BCFossilsDescriptors._collected_fossils_node.nodeid
        ).values_list('resourceinstanceidto', flat=True)

        for child_values in values_config:
            tiles = models.TileModel.objects.filter(
                nodegroup_id=child_values["node"].nodegroup_id,
                resourceinstance_id__in=fossil_sample_values
            ).all()

            if len(tiles) != 0:
                datatype = self._get_datatype_factory().get_instance(child_values["node"].datatype)

                values = []
                for tile in tiles:
                    period_value = datatype.get_display_value(tile, child_values["node"])
                    if period_value:
                        values.append(period_value)

                if len(values) > 0:
                    return_values[child_values["label"]] = ', '.join(list(set(values)))
        return return_values

    def _get_site_name(self, resource):
        display_value = "("

        start_date_node = models.Node.objects.filter(graph=resource.graph_id) .filter(name="Collection Start Year") .first()
        end_date_node = models.Node.objects.filter(graph=resource.graph_id) .filter(name="Collection End Year") .first()
        geographical_node = models.Node.objects.filter(graph=resource.graph_id) .filter(name="Geographical Name") .first()

        if start_date_node:
            value = self._get_value_from_node(
                start_date_node, resource.resourceinstanceid
            )
        else:
            value = "?"
        display_value += value if value else "?"

        if end_date_node:
            value = self._get_value_from_node(
                end_date_node, resource.resourceinstanceid
            )
        else:
            value = "?"
        display_value += (", " + value) if value else ""
        display_value += ") - "

        if geographical_node:
            value = self._get_value_from_node(
                geographical_node, resource.resourceinstanceid
            )
        else:
            value = "Unknown"
        display_value += value if value else "?"

        return display_value

    def _format_value(self, name, value, config):
        if config["show_name"]:
            return "%s: <b>%s</b>" % (name, value)
        return value

    def _nodeid_to_sequence(self, id_list, row):
        return id_list.index(row.nodeid)
