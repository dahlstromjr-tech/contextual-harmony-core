from dataclasses import asdict
from typing import Dict, Any, Optional

from src.python.pillar_router import SevenPillarArbiterRouter, AxiomPolicy
from src.python.interceptor import ModelContextProtocolInterceptor


class AxiomClientWrapper:
    """Unified entry wrapper that routes prompts through SevenPillarArbiterRouter and MCP interception."""

    def __init__(
        self,
        policy: Optional[AxiomPolicy] = None,
        default_zone: str = "Zone_B",
        default_pillar: int = 3,
    ):
        self.router = SevenPillarArbiterRouter(policy=policy, default_pillar=default_pillar)
        self.interceptor = ModelContextProtocolInterceptor(
            default_zone=default_zone,
            background_arbiter_always_on=True,
        )

    def handle_prompt(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        ctx = dict(context or {})
        route_decision = self.router.route_query(prompt, ctx)

        # Pass inferred primary domain if not explicitly set, unless in lightweight lookup mode
        interceptor_ctx = dict(ctx)
        if not route_decision.requires_pillar_lookup:
            interceptor_ctx.setdefault("domain", "external_lookup")
        elif "domain" not in interceptor_ctx and route_decision.pillar_name:
            interceptor_ctx["domain"] = route_decision.pillar_name.lower().replace(" & ", "_").replace(", ", "_").replace(" ", "_")

        uns_context = self.interceptor.map_to_uns(prompt, interceptor_ctx)

        return {
            "prompt": prompt,
            "route": asdict(route_decision),
            "uns": {
                "domain": uns_context.domain,
                "entity": uns_context.entity,
                "sensitivity_zone": uns_context.sensitivity_zone,
                "uns_path": uns_context.metadata.get("uns_path"),
                "directives": uns_context.metadata.get("directives"),
                "cross_pillar_synthesis": uns_context.metadata.get("cross_pillar_synthesis"),
            },
        }
