from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class AxiomPolicy:
    reject_shortest_path: bool = True
    protect_cognitive_sanctuary: bool = True
    weigh_human_intent: bool = True
    background_arbiter_always_on: bool = True


@dataclass
class PillarRouteDecision:
    pillar_id: Optional[int]
    pillar_name: Optional[str]
    uns_path: str
    requires_pillar_lookup: bool
    retrieval_order: List[str]
    axiom_flags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


PILLAR_REGISTRY: Dict[int, str] = {
    1: "Physical State & Recovery",
    2: "Health & Nutrition",
    3: "Mind, Attention & Contextual Harmony",
    4: "Purpose, Work & Mission",
    5: "Finances & Resources",
    6: "Relationships & Community",
    7: "Environmental, Gear & Exploration",
}

DOMAIN_TO_PILLAR: Dict[str, int] = {
    "recovery": 1,
    "physical_state": 1,
    "health": 2,
    "nutrition": 2,
    "mental_health": 3,
    "attention": 3,
    "contextual_harmony": 3,
    "mission": 4,
    "work": 4,
    "purpose": 4,
    "finances": 5,
    "resources": 5,
    "relationships": 6,
    "community": 6,
    "environment": 7,
    "gear": 7,
    "exploration": 7,
}


class SevenPillarArbiterRouter:
    """Keeps Background Arbiter active on all queries while supporting lightweight bypass for unanchored lookups."""

    def __init__(self, policy: Optional[AxiomPolicy] = None, default_pillar: int = 3):
        self.policy = policy or AxiomPolicy()
        self.default_pillar = default_pillar

    def route_query(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> PillarRouteDecision:
        ctx = context or {}
        domain = ctx.get("domain")
        entity = ctx.get("entity", "general").lower().replace(" ", "_")

        axiom_flags: List[str] = []
        if self.policy.background_arbiter_always_on:
            axiom_flags.append("BACKGROUND_ARBITER_ACTIVE")
        if self.policy.weigh_human_intent:
            axiom_flags.append("INTENT_WEIGHTED_EVALUATION")
        if self.policy.reject_shortest_path and ctx.get("shortcut_risk", False):
            axiom_flags.append("SHORTEST_PATH_FALLACY_CHECK")

        is_lightweight_lookup = bool(ctx.get("lightweight_lookup", False)) and not domain
        if is_lightweight_lookup:
            return PillarRouteDecision(
                pillar_id=None,
                pillar_name=None,
                uns_path=f"/uns/lightweight/external/{entity}",
                requires_pillar_lookup=False,
                retrieval_order=["external_web_evaluated_via_axiom"],
                axiom_flags=axiom_flags,
                metadata={
                    "internal_first": False,
                    "lightweight_mode": True,
                    "urgency_weight": ctx.get("urgency_weight", 0.2),
                },
            )

        resolved_domain = (domain or "contextual_harmony").lower()
        pillar_id = DOMAIN_TO_PILLAR.get(resolved_domain, self.default_pillar)
        pillar_name = PILLAR_REGISTRY[pillar_id]

        if self.policy.protect_cognitive_sanctuary and pillar_id == 3:
            axiom_flags.append("SANCTUARY_AWARENESS_ACTIVE")

        retrieval_order = ["internal_pillar_notebook", "related_pillars"]
        if ctx.get("allow_external_web", True):
            retrieval_order.append("external_web_evaluated_via_axiom")

        return PillarRouteDecision(
            pillar_id=pillar_id,
            pillar_name=pillar_name,
            uns_path=f"/uns/pillar_{pillar_id}/{resolved_domain}/{entity}",
            requires_pillar_lookup=True,
            retrieval_order=retrieval_order,
            axiom_flags=axiom_flags,
            metadata={
                "internal_first": True,
                "lightweight_mode": False,
                "urgency_weight": ctx.get("urgency_weight", 0.5),
            },
        )
