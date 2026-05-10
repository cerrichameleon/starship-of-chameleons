from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from .runtime_manifest import build_runtime_manifest

if TYPE_CHECKING:
    from .runtime import StarshipRuntime


@dataclass
class CaptainProposedRole:
    role_name: str
    reason: str
    focus_area: str = "general"
    group_tags: list[str] = field(default_factory=list)
    reports_to_role_name: str | None = None


@dataclass
class CaptainCrewProposal:
    mission_prompt: str
    rationale: str
    proposed_roles: list[CaptainProposedRole] = field(default_factory=list)
    research_notes: list[str] = field(default_factory=list)
    approval_status: str = "draft"


class CaptainConsole:
    """Interface-independent Captain-facing application service."""

    def __init__(self, runtime: StarshipRuntime) -> None:
        self.runtime = runtime

    def get_startup_manifest_lines(self) -> list[str]:
        return build_runtime_manifest(self.runtime).summary_lines

    def submit_chat_message(self, message_text: str) -> str:
        reply = self.runtime.captain_chat_session.talk_to_captain(message_text)
        captain = self.runtime.starship.captain
        provider_id = captain.brain_profile.get("provider_id", "unknown")
        estimated_input_tokens = max(1, len(message_text) // 4)
        estimated_output_tokens = max(1, len(reply) // 4)
        estimated_cost_usd = (estimated_input_tokens + estimated_output_tokens) * 0.00001
        self.runtime.activity_log_store.append_entry(
            actor_id=captain.chameleon_id,
            actor_name=captain.name,
            event_type="captain-chat",
            message="Captain handled a user chat turn.",
            metadata={
                "provider_id": provider_id,
                "estimated_input_tokens": estimated_input_tokens,
                "estimated_output_tokens": estimated_output_tokens,
                "estimated_cost_usd": estimated_cost_usd,
            },
        )
        self.runtime.usage_tracker.record_usage(
            actor_id=captain.chameleon_id,
            actor_name=captain.name,
            provider_id=provider_id,
            estimated_input_tokens=estimated_input_tokens,
            estimated_output_tokens=estimated_output_tokens,
            estimated_cost_usd=estimated_cost_usd,
            metadata={"event_type": "captain-chat"},
        )
        return reply

    def summarize_chat_history(self) -> list[dict[str, str]]:
        return [
            {"role": turn.role, "text": turn.text}
            for turn in self.runtime.captain_chat_session.history
        ]

    def draft_crew_proposal(self, mission_prompt: str) -> CaptainCrewProposal:
        captain_reply = self.runtime.starship.captain.think(
            mission="design an appropriate crew structure for a new mission",
            channel_status="captain's console planning mode",
            user_message=(
                "Analyze the following mission request, infer a suitable initial crew structure, and explain your reasoning. "
                "Do not instantiate crew yet. Produce a concise rationale plus a role list.\n\n"
                f"Mission request: {mission_prompt}"
            ),
        )
        proposed_roles = self._infer_proposed_roles(captain_reply)
        return CaptainCrewProposal(
            mission_prompt=mission_prompt,
            rationale=captain_reply,
            proposed_roles=proposed_roles,
            research_notes=[],
            approval_status="draft",
        )

    def _infer_proposed_roles(self, captain_reply: str) -> list[CaptainProposedRole]:
        role_patterns = [
            ("software project manager", "software-management", ["software", "management"], None),
            ("project manager", "management", ["management"], None),
            ("scrum master", "software-management", ["software", "management"], "software-project-manager"),
            ("ui coder", "software", ["software", "ui"], "software-project-manager"),
            ("backend coder", "software", ["software", "backend"], "software-project-manager"),
            ("software engineer", "software", ["software"], None),
            ("artist", "art", ["art"], None),
            ("qa", "qa", ["qa", "oxpecker"], None),
            ("operations", "ops", ["ops"], None),
        ]
        lower_reply = captain_reply.lower()
        proposed_roles: list[CaptainProposedRole] = []
        for phrase, focus_area, group_tags, reports_to_role_name in role_patterns:
            if phrase in lower_reply:
                proposed_roles.append(
                    CaptainProposedRole(
                        role_name=phrase.replace(" ", "-"),
                        reason=f"Captain identified '{phrase}' as useful for this mission.",
                        focus_area=focus_area,
                        group_tags=group_tags,
                        reports_to_role_name=reports_to_role_name,
                    )
                )
        if not proposed_roles:
            proposed_roles.append(
                CaptainProposedRole(
                    role_name="general-specialist",
                    reason="Captain did not name concrete roles, so a general specialist was proposed as a safe fallback.",
                    focus_area="general",
                    group_tags=["general"],
                )
            )
        return proposed_roles
