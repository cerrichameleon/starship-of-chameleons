from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .runtime import StarshipRuntime


@dataclass
class RuntimeManifest:
    ship_name: str
    ship_class: str
    captain_name: str
    active_provider: str
    active_model: str
    access_path: str
    credentials_ref: str
    fallback_order: list[str] = field(default_factory=list)
    selected_provider_order: list[str] = field(default_factory=list)
    using_tokens: bool = False
    crew_count: int = 0
    crew_names: list[str] = field(default_factory=list)
    drydock_state: str = "unknown"
    mission_status: str = "unknown"
    warnings: list[str] = field(default_factory=list)
    summary_lines: list[str] = field(default_factory=list)


def build_runtime_manifest(runtime: "StarshipRuntime") -> RuntimeManifest:
    captain = runtime.starship.captain
    captain_profile = captain.brain_profile
    crew_entries = list(runtime.starship.crew_registry.list_entries())
    warnings: list[str] = []

    active_provider = captain_profile.get("provider_label") or captain_profile.get("provider_id", "unknown")
    active_model = captain_profile.get("model_id", "unknown")
    access_path = captain_profile.get("access_path", "unknown")
    credentials_ref = captain_profile.get("credentials_ref", "unknown")
    using_tokens = access_path == "api-key"

    if not captain.has_brain():
        warnings.append("Captain brain not assigned.")
    if runtime.drydock_controller.is_in_drydock():
        drydock_state = "drydock"
    else:
        drydock_state = "launched"

    mission_status = "active mission" if runtime.captain_chat_session.history else "ready for orders"

    selected_provider_order = list(captain_profile.get("selected_provider_order", []))

    manifest = RuntimeManifest(
        ship_name=runtime.starship.name,
        ship_class=runtime.starship.ship_class,
        captain_name=captain.name,
        active_provider=active_provider,
        active_model=active_model,
        access_path=access_path,
        credentials_ref=credentials_ref,
        fallback_order=["codex", "openai-api", "gemini-api"],
        selected_provider_order=selected_provider_order,
        using_tokens=using_tokens,
        crew_count=len(crew_entries),
        crew_names=[
            runtime.starship.crew_registry.get_chameleon(entry.entity_id).name
            for entry in crew_entries
            if runtime.starship.crew_registry.get_chameleon(entry.entity_id) is not None
        ],
        drydock_state=drydock_state,
        mission_status=mission_status,
        warnings=warnings,
    )
    crew_label = ", ".join(manifest.crew_names) if manifest.crew_names else "none"
    bridge_readiness = "ready for live Captain chat" if captain.has_brain() else "Captain brain missing"
    manifest.summary_lines = [
        f"ship: {manifest.ship_name} ({manifest.ship_class})",
        f"captain: {manifest.captain_name}",
        f"provider: {manifest.active_provider}",
        f"model: {manifest.active_model}",
        f"access: {manifest.access_path}",
        f"credentials: {manifest.credentials_ref}",
        f"fallback order: {', '.join(manifest.fallback_order)}",
        f"selected provider order: {', '.join(manifest.selected_provider_order) if manifest.selected_provider_order else 'ambient default'}",
        f"using tokens: {'yes' if manifest.using_tokens else 'no'}",
        f"crew assigned: {manifest.crew_count}",
        f"crew roster: {crew_label}",
        f"ship state: {manifest.drydock_state}",
        f"mission state: {manifest.mission_status}",
        f"bridge readiness: {bridge_readiness}",
    ]
    if manifest.warnings:
        manifest.summary_lines.append("warnings: " + " | ".join(manifest.warnings))
    return manifest
