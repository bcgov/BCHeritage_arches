import json
import logging

from arches.app.datatypes.datatypes import StringDataType
from arches.app.models import models
import re
from bcrhp.util.borden_number_api import BordenNumberApi

borden_number_widget = models.Widget.objects.get(name="borden-number-widget")

details = {
    "datatype": "borden-number-datatype",
    "iconclass": "fa fa-file-code-o",
    "modulename": "borden_number_datatype.py",
    "classname": "BordenNumberDataType",
    "defaultwidget": borden_number_widget,
    "defaultconfig": {"format": "AaAa-000", "pgDatatype": "jsonb"},
    "configcomponent": "views/components/datatypes/string",
    "configname": "string-datatype-config",
    "isgeometric": False,
    "issearchable": True,
}

logger = logging.getLogger(__name__)


class BordenNumberDataType(StringDataType):
    borden_number_format = re.compile("^[A-Z][a-z][A-Z][a-z]-\\d{1,4}$")
    bn_api = BordenNumberApi()

    def validate(
        self,
        value,
        row_number=None,
        source=None,
        node=None,
        nodeid=None,
        strict=False,
        **kwargs
    ):
        errors = super(BordenNumberDataType, self).validate(
            value, row_number, source, node, nodeid, strict, **kwargs
        )
        resource_id = None

        if (
            kwargs["request"]
            and kwargs["request"].POST
            and kwargs["request"].POST.get("data")
        ):
            dict = json.JSONDecoder().decode(kwargs["request"].POST.get("data"))
            if dict is not None:
                resource_id = dict["resourceinstance_id"]

        logger.debug("Validating for resource instance id %s" % resource_id)
        try:
            if value is not None:
                result = self.borden_number_format.match(value["en"]["value"])
                if not result:
                    errors.append(
                        {
                            "type": "ERROR",
                            "message": "Invalid borden number format: {0}. Valid format is: {1}. {2}".format(
                                value["en"]["value"],
                                self.datatype_model.defaultconfig["format"],
                                "This data was not imported.",
                            ),
                        }
                    )
                elif resource_id:
                    try:
                        logger.debug("Values: %s, %s" % (value, resource_id))
                        logger.debug("Validating BN existence in validate()")
                        if self.bn_api.validate_borden_number(
                            value["en"]["value"], resource_id
                        ):
                            errors.append(
                                {
                                    "type": "ERROR",
                                    "message": "Borden Number already exists.",
                                }
                            )
                    except Exception as e:
                        errors.append({"type": "ERROR", "message": str(e)})
        except Exception as e:
            print(e)
            errors.append(
                {
                    "type": "ERROR",
                    "message": "datatype: {0} value: {1} Exception: {2}".format(
                        self.datatype_model.datatype, value, e
                    ),
                }
            )
        return errors

    def clean(self, tile, nodeid):
        """
        Enforces AbCd-999 format
        """
        super(BordenNumberDataType, self).clean(tile, nodeid)
        if tile.data[nodeid] is None or tile.data[nodeid]["en"] is None:
            print("Bypassing clean...")
            return

        borden_number = tile.data[nodeid]["en"]["value"]
        if borden_number is not None and len(borden_number) >= 6:
            tile.data[nodeid]["en"]["value"] = (
                re.sub(r"(.{2})(.{2})", r"\1 \2", borden_number, 1)
                .title()
                .replace(" ", "")
            )

    def post_tile_save(self, tile, nodeid, request):
        # This needs to happen after the save as we can't rollback the HRIA transaction after it is done.
        # @todo - Should look into whether we can actually create the record in HRIA before the save and commit after

        logger.debug("Tile: %s" % tile.data)
        value = tile.data[nodeid]["en"]["value"]
        # print("Saving %s:%s" % (tile.resourceinstance_id, value))
        logger.debug(
            "Trying to reserve borden number %s for %s"
            % (value, tile.resourceinstance_id)
        )
        self.bn_api.reserve_borden_number(value, tile.resourceinstance_id)

    # def transform_export_values(self, value, *args, **kwargs):
    #     super(BordenNumberDataType, self).transform_export_values(value, args, kwargs)
    #     if value is not None:
    #         return value.encode("utf8")

    # def get_search_terms(self, nodevalue, nodeid=None):
    #     terms = []
    #     if nodevalue is not None and isinstance(nodevalue, dict):
    #         if settings.WORDS_PER_SEARCH_TERM is None or (len(nodevalue[key]["value"].split(" ")) < settings.WORDS_PER_SEARCH_TERM):
    #             terms.append(SearchTerm(value=nodevalue[key]["value"], lang=key))
    #     return terms

    # def append_search_filters(self, value, node, query, request):
    #     try:
    #         if value["val"] != "":
    #             match_type = "phrase_prefix" if "~" in value["op"] else "phrase"
    #             match_query = Match(field="tiles.data.%s" % (str(node.pk)), query=value["val"], type=match_type)
    #             if "!" in value["op"]:
    #                 query.must_not(match_query)
    #                 query.filter(Exists(field="tiles.data.%s" % (str(node.pk))))
    #             else:
    #                 query.must(match_query)
    #     except KeyError as e:
    #         pass
