import unittest
from src.python.axiom_entry import AxiomClientWrapper


class TestAxiomClientWrapper(unittest.TestCase):
    def setUp(self):
        self.wrapper = AxiomClientWrapper()

    def test_lightweight_lookup_bypasses_pillar_retrieval_with_axiom_active(self):
        result = self.wrapper.handle_prompt(
            "What is the temperature in Bangkok today?",
            {"entity": "bangkok_temp", "lightweight_lookup": True},
        )
        self.assertFalse(result["route"]["requires_pillar_lookup"])
        self.assertIsNone(result["route"]["pillar_id"])
        self.assertIn("BACKGROUND_ARBITER_ACTIVE", result["route"]["axiom_flags"])
        self.assertIn("BACKGROUND_ARBITER_ACTIVE", result["uns"]["cross_pillar_synthesis"]["axiom_flags"])

    def test_cross_pillar_synthesis_and_zone_routing(self):
        result = self.wrapper.handle_prompt(
            "Balance recovery pacing with mission work",
            {
                "domain": "recovery",
                "entity": "pacing",
                "related_pillars": [4],
                "shortcut_risk": True,
            },
        )
        self.assertTrue(result["route"]["requires_pillar_lookup"])
        self.assertEqual(result["route"]["pillar_id"], 1)
        self.assertEqual(result["uns"]["sensitivity_zone"], "Zone_B")
        self.assertEqual(
            result["uns"]["cross_pillar_synthesis"]["retrieval_order"],
            ["internal_pillar_1", "internal_pillar_4", "external_web_evaluated_via_axiom"],
        )
        self.assertIn("SHORTEST_PATH_FALLACY_CHECK", result["uns"]["cross_pillar_synthesis"]["axiom_flags"])

    def test_zone_c_sanctuary_protection_through_wrapper(self):
        result = self.wrapper.handle_prompt(
            "Processing personal reflection notes",
            {"domain": "mental_health", "entity": "reflection"},
        )
        self.assertEqual(result["route"]["pillar_id"], 3)
        self.assertEqual(result["uns"]["sensitivity_zone"], "Zone_C")
        self.assertTrue(result["uns"]["directives"]["sanctuary_mode"])
        self.assertTrue(result["uns"]["directives"]["ai_generation_prohibited"])


if __name__ == "__main__":
    unittest.main()
