from arches.app.datatypes.datatypes import StringDataType
from arches.app.models import models
from arches.app.models.system_settings import settings
from arches.app.search.elasticsearch_dsl_builder import Bool, Match, Range, Term, Terms, Nested, Exists, RangeDSLException
from arches.app.search.search_term import SearchTerm
import re

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


class BordenNumberDataType(StringDataType):
    borden_number_format = re.compile('[A-Z][a-z][A-Z][a-z]-\d{1,3}')

    def validate(self, value, row_number=None, source=None, node=None, nodeid=None, strict=False, **kwargs):
        errors = super(BordenNumberDataType, self).validate(value, row_number, source, node, nodeid, strict, **kwargs)
        try:
            if value is not None:
                for key in value.keys():
                    if not self.borden_number_format.match(value[key]):
                        errors.append(
                            {
                                "type": "ERROR",
                                "message": "Invalid borden number format: {0}. Valid format is: {1}. {2}".format(
                                    value,
                                    self.datatype_model.defaultconfig['format'],
                                    "This data was not imported."
                                ),
                            }
                        )

        except Exception as e:
            print(e)
            errors.append(
                {
                    "type": "ERROR",
                    "message": "datatype: {0} value: {1} Exception: {2}".format(
                        self.datatype_model.datatype,
                        value,
                        e
                    ),
                }
            )
        return errors

    def clean(self, tile, nodeid):
        """
        Enforces AbCd-999 format
        """
        super(BordenNumberDataType, self).clean(tile, nodeid)
        if tile.data[nodeid] is not None and len(tile.data[nodeid]) >= 6:
            tile.data[nodeid] = re.sub(r"(.{2})(.{2})", r"\1 \2", tile.data[nodeid], 1).title().replace(" ","")

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
