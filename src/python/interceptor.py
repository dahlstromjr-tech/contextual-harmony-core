import json
import logging
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MCPInterceptor")

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


@dataclass
class NamespaceContext:
    domain: str
    entity: str
    sensitivity_zone: str
    raw_payload: str
    metadata: Dict[str, Any]


@dataclass
class CrossPillarSynthesisPlan:
    primary_pillar_id: int
    primary_pillar_name: str
    synthesized_pillars: List[Dict[str, Any]]
    retrieval_order: List[str]
    axiom_flags: List[str] = field(default_factory=list)


class ModelContextProtocolInterceptor:
    """Intercepts raw tool inputs, normalizes them into UNS paths, and supports cross-pillar synthesis."""

    def __init__(self, default_zone: str = "Zone_B", background_arbiter_always_on: bool = True):
        self.default_zone = default_zone
        self.background_arbiter_always_on = background_arbiter_always_on

    def map_to_uns(self, raw_input: str, context_metadata: Optional[Dict[str, Any]] = None) -> NamespaceContext:
        ctx = context_metadata or {}
        domain = ctx.get("domain", "general")
        entity = ctx.get("entity", "unclassified")

        if ctx.get("empathy_required", False) or domain == "mental_health":
            zone = "Zone_C"
        elif domain in ["logistics", "inventory", "routing"]:
            zone = "Zone_A"
        else:
            zone = self.default_zone

        synthesis = self.plan_cross_pillar_synthesis(raw_input, ctx)

        return NamespaceContext(
            domain=domain,
            entity=entity,
            sensitivity_zone=zone,
            raw_payload=raw_input,
            metadata={
                "interceptor_version": "2.1.0",
                "uns_path": f"/uns/{zone}/{domain}/{entity}",
                "bidirectional_weight": ctx.get("human_urgency_weight", 0.5),
                "directives": self._get_directives(zone),
                "cross_pillar_synthesis": asdict(synthesis),
            },
        )

    def plan_cross_pillar_synthesis(
        self, raw_input: str, context_metadata: Optional[Dict[str, Any]] = None
    ) -> CrossPillarSynthesisPlan:
        ctx = context_metadata or {}
        primary_domain = ctx.get("domain", "contextual_harmony").lower()
        primary_pillar_id = DOMAIN_TO_PILLAR.get(primary_domain, 3)

        ordered_pillar_ids: List[int] = [primary_pillar_id]
        for pid in ctx.get("related_pillars", []):
            if pid in PILLAR_REGISTRY and pid not in ordered_pillar_ids:
                ordered_pillar_ids.append(pid)
        for sec_domain in ctx.get("secondary_domains", []):
            sec_pid = DOMAIN_TO_PILLAR.get(sec_domain.lower())
            if sec_pid and sec_pid not in ordered_pillar_ids:
                ordered_pillar_ids.append(sec_pid)

        synthesized_pillars = [
            {
                "pillar_id": pid,
                "pillar_name": PILLAR_REGISTRY[pid],
                "role": "primary" if pid == primary_pillar_id else "secondary_synthesis",
                "pillar_path": f"/uns/pillar_{pid}/{PILLAR_REGISTRY[pid].lower().replace(' & ', '_').replace(', ', '_').replace(' ', '_')}",
            }
            for pid in ordered_pillar_ids
        ]

        retrieval_order = [f"internal_pillar_{pid}" for pid in ordered_pillar_ids]
        if ctx.get("allow_external_web", True):
            retrieval_order.append("external_web_evaluated_via_axiom")

        axiom_flags: List[str] = ["INTENT_WEIGHTED_EVALUATION"]
        if self.background_arbiter_always_on:
            axiom_flags.insert(0, "BACKGROUND_ARBITER_ACTIVE")
        if ctx.get("shortcut_risk", False):
            axiom_flags.append("SHORTEST_PATH_FALLACY_CHECK")
        if 3 in ordered_pillar_ids:
            axiom_flags.append("SANCTUARY_AWARENESS_ACTIVE")

        return CrossPillarSynthesisPlan(
            primary_pillar_id=primary_pillar_id,
            primary_pillar_name=PILLAR_REGISTRY[primary_pillar_id],
            synthesized_pillars=synthesized_pillars,
            retrieval_order=retrieval_order,
            axiom_flags=axiom_flags,
        )

    def _get_directives(self, zone: str) -> Dict[str, Any]:
        if zone == "Zone_A":
            return {"autonomous_adaptation": True}
        if zone == "Zone_B":
            return {"human_checkpoint": True}
        return {"ai_generation_prohibited": True, "sanctuary_mode": True}
