import unittest
from src.python.pillar_router import SevenPillarArbiterRouter


class TestSevenPillarArbiterRouter(unittest.TestCase):
    def setUp(self):
        self.router = SevenPillarArbiterRouter()

    def test_internal_first_order_on_gear_query(self):
        decision = self.router.route_query(
            "Check trail gear setup and weather conditions",
            {"domain": "gear", "entity": "trail_kit", "shortcut_risk": True},
        )
        self.assertEqual(decision.pillar_id, 7)
        self.assertTrue(decision.requires_pillar_lookup)
        self.assertEqual(decision.retrieval_order[0], "internal_pillar_notebook")
        self.assertEqual(decision.retrieval_order[-1], "external_web_evaluated_via_axiom")
        self.assertIn("BACKGROUND_ARBITER_ACTIVE", decision.axiom_flags)
        self.assertIn("SHORTEST_PATH_FALLACY_CHECK", decision.axiom_flags)

    def test_pillar_3_sanctuary_flag(self):
        decision = self.router.route_query(
            "Review attention pacing rules",
            {"domain": "attention", "entity": "ais_state"},
        )
        self.assertEqual(decision.pillar_id, 3)
        self.assertTrue(decision.requires_pillar_lookup)
        self.assertIn("BACKGROUND_ARBITER_ACTIVE", decision.axiom_flags)
        self.assertIn("SANCTUARY_AWARENESS_ACTIVE", decision.axiom_flags)

    def test_lightweight_bypass_keeps_background_arbiter_active(self):
        decision = self.router.route_query(
            "What is the temperature in Bangkok today?",
            {"entity": "bangkok_temperature", "lightweight_lookup": True},
        )
        self.assertIsNone(decision.pillar_id)
        self.assertFalse(decision.requires_pillar_lookup)
        self.assertEqual(decision.retrieval_order, ["external_web_evaluated_via_axiom"])
        self.assertIn("BACKGROUND_ARBITER_ACTIVE", decision.axiom_flags)
        self.assertTrue(decision.metadata["lightweight_mode"])


if __name__ == "__main__":
    unittest.main()
