import unittest
from src.python.interceptor import ModelContextProtocolInterceptor

class TestModelContextProtocolInterceptor(unittest.TestCase):
    def setUp(self):
        self.interceptor = ModelContextProtocolInterceptor()

    def test_zone_a_routing(self):
        context = self.interceptor.map_to_uns("Shipment batch #402", {"domain": "logistics", "entity": "shipping"})
        self.assertEqual(context.sensitivity_zone, "Zone_A")
        self.assertTrue(context.metadata["directives"]["autonomous_adaptation"])

    def test_zone_c_sanctuary(self):
        context = self.interceptor.map_to_uns("Processing personal reflection", {"domain": "mental_health", "entity": "user_mindset"})
        self.assertEqual(context.sensitivity_zone, "Zone_C")
        self.assertTrue(context.metadata["directives"]["sanctuary_mode"])

    def test_zone_b_default(self):
        context = self.interceptor.map_to_uns("General inquiry", {"domain": "general", "entity": "chat"})
        self.assertEqual(context.sensitivity_zone, "Zone_B")
        self.assertTrue(context.metadata["directives"]["human_checkpoint"])

if __name__ == "__main__":
    unittest.main()
