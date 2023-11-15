# from tests.base_test import ArchesTestCase
from django.test.runner import DiscoverRunner,TestCase
from bcfms.util.scientific_terms_util import ScientificTermsFormatter

class ActivityStreamCollectionTests(TestCase):
    sci_formats = [
        {"parts": {"name": "Genus", "open_nom": None, "other_name": None }, "expected": "Genus sp."},
        {"parts": {"name": "Emeraldella brocki", "open_nom": None, "other_name": None }, "expected": "Emeraldella brocki"},
        {"parts": {"name": "Petalaxis", "open_nom": "cf.", "other_name": "Petalaxis sutherlandi"}, "expected": "Petalaxis cf. Petalaxis sutherlandi"},
        {"parts": {"name": None, "open_nom": "ex. aff.", "other_name": "Hemihoplites soulieri"}, "expected": "ex. aff. Hemihoplites soulieri"},
    ]

    times_formats = [
        {"parts": {"min": "Jurassic", "min_uncertain": None, "max": None, "max_uncertain": None}, "expected": "Jurassic -"},
        {"parts": {"min": "Jurassic", "min_uncertain": False, "max": None, "max_uncertain": None}, "expected": "Jurassic -"},
        {"parts": {"min": "Jurassic", "min_uncertain": True, "max": None, "max_uncertain": None}, "expected": "Jurassic ? -"},
        {"parts": {"min": "Jurassic", "min_uncertain": None, "max": "Triassic", "max_uncertain": None}, "expected": "Jurassic - Triassic"},
        {"parts": {"min": "Jurassic", "min_uncertain": False, "max": "Triassic", "max_uncertain": False}, "expected": "Jurassic - Triassic"},
        {"parts": {"min": "Jurassic", "min_uncertain": True, "max": "Triassic", "max_uncertain": False}, "expected": "Jurassic ? - Triassic"},
        {"parts": {"min": "Jurassic", "min_uncertain": True, "max": "Triassic", "max_uncertain": True}, "expected": "Jurassic ? - Triassic ?"},
        {"parts": {"min": "Jurassic", "min_uncertain": False, "max": "Triassic", "max_uncertain": True}, "expected": "Jurassic - Triassic ?"},
        {"parts": {"min": None, "min_uncertain": None, "max": "Triassic", "max_uncertain": False}, "expected": " - Triassic"},
        {"parts": {"min": None, "min_uncertain": None, "max": "Triassic", "max_uncertain": True}, "expected": " - Triassic ?"},
    ]

    def test_scientific_name_formatting(self):
        for sci_format in self.sci_formats:
            self.assertEqual(ScientificTermsFormatter.format_scientific_name(
                sci_format["parts"]["name"],
                sci_format["parts"]["open_nom"],
                sci_format["parts"]["other_name"]),
                sci_format["expected"])

    def test_uncertain_formatting(self):
        self.assertEqual(ScientificTermsFormatter.format_uncertain("certain", False), "certain")
        self.assertEqual(ScientificTermsFormatter.format_uncertain("uncertain", True), "uncertain ?")
        self.assertEqual(ScientificTermsFormatter.format_uncertain("should be uncertain", True), "should be uncertain ?")

    def test_format_times(self):
        for time_format in self.times_formats:
            self.assertEqual(ScientificTermsFormatter.format_times(time_format["parts"]["min"],
                                                                   time_format["parts"]["min_uncertain"],
                                                                   time_format["parts"]["max"],
                                                                   time_format["parts"]["max_uncertain"],
                                                                   ), time_format["expected"])
