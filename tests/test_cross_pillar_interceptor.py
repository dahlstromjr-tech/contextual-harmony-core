import unittest
from src.python.interceptor import ModelContextProtocolInterceptor


class TestCrossPillarInterceptor(unittest.TestCase):
    def setUp(self):
        self.interceptor = ModelContextProtocolInterceptor()

    def test_cross_pillar_recovery_and_mission_synthesis(self):
        ctx_out = self.interceptor.map_to_uns(
            "Balance recovery pacing with upcoming mission deliverables",
            {
                "domain": "recovery",
                "entity": "recovery_vs_mission",
                "related_pillars": [4],
                "shortcut_risk": True,
            },
        )
        synthesis = ctx_out.metadata["cross_pillar_synthesis"]
        self.assertEqual(synthesis["primary_pillar_id"], 1)
        self.assertEqual(len(synthesis["synthesized_pillars"]), 2)
        self.assertEqual(synthesis["synthesized_pillars"][1]["pillar_id"], 4)
        self.assertEqual(
            synthesis["retrieval_order"],
            ["internal_pillar_1", "internal_pillar_4", "external_web_evaluated_via_axiom"],
        )
        self.assertIn("BACKGROUND_ARBITER_ACTIVE", synthesis["axiom_flags"])
        self.assertIn("SHORTEST_PATH_FALLACY_CHECK", synthesis["axiom_flags"])


if __name__ == "__main__":
    unittest.main()
