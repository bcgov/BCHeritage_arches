# from tests.base_test import ArchesTestCase
from django.test.runner import DiscoverRunner, TestCase
from bcrhp.util.crhp_xml_generator import CrhpXmlGenerator


class CrhpXmlGeneratorTests(TestCase):
    sci_formats = [
        {
            "parts": {"name": "Genus", "open_nom": None, "other_name": None},
            "expected": "Genus sp.",
        },
        {
            "parts": {
                "name": "Emeraldella brocki",
                "open_nom": None,
                "other_name": None,
            },
            "expected": "Emeraldella brocki",
        },
        {
            "parts": {
                "name": "Petalaxis",
                "open_nom": "cf.",
                "other_name": "Petalaxis sutherlandi",
            },
            "expected": "Petalaxis cf. Petalaxis sutherlandi",
        },
        {
            "parts": {
                "name": None,
                "open_nom": "ex. aff.",
                "other_name": "Hemihoplites soulieri",
            },
            "expected": "ex. aff. Hemihoplites soulieri",
        },
    ]

    times_formats = [
        {
            "parts": {
                "min": "Jurassic",
                "min_uncertain": None,
                "max": None,
                "max_uncertain": None,
            },
            "expected": "Jurassic -",
        },
        {
            "parts": {
                "min": "Jurassic",
                "min_uncertain": False,
                "max": None,
                "max_uncertain": None,
            },
            "expected": "Jurassic -",
        },
        {
            "parts": {
                "min": "Jurassic",
                "min_uncertain": True,
                "max": None,
                "max_uncertain": None,
            },
            "expected": "Jurassic ? -",
        },
        {
            "parts": {
                "min": "Jurassic",
                "min_uncertain": None,
                "max": "Triassic",
                "max_uncertain": None,
            },
            "expected": "Jurassic - Triassic",
        },
        {
            "parts": {
                "min": "Jurassic",
                "min_uncertain": False,
                "max": "Triassic",
                "max_uncertain": False,
            },
            "expected": "Jurassic - Triassic",
        },
        {
            "parts": {
                "min": "Jurassic",
                "min_uncertain": True,
                "max": "Triassic",
                "max_uncertain": False,
            },
            "expected": "Jurassic ? - Triassic",
        },
        {
            "parts": {
                "min": "Jurassic",
                "min_uncertain": True,
                "max": "Triassic",
                "max_uncertain": True,
            },
            "expected": "Jurassic ? - Triassic ?",
        },
        {
            "parts": {
                "min": "Jurassic",
                "min_uncertain": False,
                "max": "Triassic",
                "max_uncertain": True,
            },
            "expected": "Jurassic - Triassic ?",
        },
        {
            "parts": {
                "min": None,
                "min_uncertain": None,
                "max": "Triassic",
                "max_uncertain": False,
            },
            "expected": " - Triassic",
        },
        {
            "parts": {
                "min": None,
                "min_uncertain": None,
                "max": "Triassic",
                "max_uncertain": True,
            },
            "expected": " - Triassic ?",
        },
    ]

    def test_generate_xml(self):
        generator = CrhpXmlGenerator()
        generator.generate_xml("123")
