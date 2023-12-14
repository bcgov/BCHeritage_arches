import re
class ScientificTermsFormatter:

    species_unknown_suffix = " sp."
    @staticmethod
    def format_scientific_name(scientific_name, open_nomenclature_term, other_scientific_name):
        formatted_name = ""
        if (scientific_name is None or scientific_name == "") and (other_scientific_name is None or other_scientific_name == ""):
            return None
        if scientific_name:
            formatted_name = scientific_name
        if open_nomenclature_term:
            formatted_name += (" " + open_nomenclature_term)
        if other_scientific_name:
            formatted_name += (" " + other_scientific_name)
        if scientific_name and not open_nomenclature_term and not other_scientific_name and not re.match(".* .*", scientific_name):
            formatted_name += ScientificTermsFormatter.species_unknown_suffix
        formatted_name = formatted_name.strip()

        return formatted_name

    @staticmethod
    def format_common_name(common_name, common_name_uncertain):
        return ScientificTermsFormatter._format_uncertain(common_name, common_name_uncertain)

    @staticmethod
    def format_times(min_time, min_time_uncertain, max_time, max_time_uncertain):
        min_time_str = ScientificTermsFormatter._format_uncertain(min_time, min_time_uncertain)
        max_time_str = ScientificTermsFormatter._format_uncertain(max_time, max_time_uncertain)
        if not min_time_str and not max_time_str:
            return None
        return ("%s - %s" % (min_time_str if min_time_str else "", max_time_str if max_time_str else "")).rstrip()

    @staticmethod
    def format_uncertain(value, is_uncertain):
        if not value:
            return None
        return ScientificTermsFormatter._format_uncertain(value, is_uncertain)

    @staticmethod
    def _format_uncertain(value, is_uncertain):
        if value:
            return "%s ?"%value if is_uncertain else value
        return None
