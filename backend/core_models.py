"""Dependency-free data objects shared by the converter pipeline.

The web application keeps its Pydantic request/response models in ``models``.
This module contains only the small runtime structures needed by the converter,
so the same conversion engine can run inside OrcaSlicer's embedded Python.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ConversionSettings:
    reference_profile: str
    apply_rules: bool = True
    clamp_speeds: bool = True
    strip_custom_gcode: bool = True
    preserve_color_painting: bool = True
    advanced_overrides: dict[str, Any] = field(default_factory=dict)
    slot_map: dict[int, int] = field(default_factory=dict)
    insert_swap_pauses: bool = False

    def model_dump(self, **_: Any) -> dict[str, Any]:
        return asdict(self)


@dataclass
class IdentitySwap:
    key: str
    from_value: Any = None
    to_value: Any = None

    def model_dump(self, **_: Any) -> dict[str, Any]:
        return asdict(self)


@dataclass
class GcodeSwapEvent:
    key: str
    from_bytes: int
    to_bytes: int

    def model_dump(self, **_: Any) -> dict[str, Any]:
        return asdict(self)


@dataclass
class KeyDropEvent:
    key: str
    reason: str = "not-in-target-schema"

    def model_dump(self, **_: Any) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ClampEvent:
    key: str
    from_value: Any
    to_value: Any
    ceiling: Any

    def model_dump(self, **_: Any) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RuleMatch:
    rule_name: str
    priority: int
    matched_on: dict[str, Any]
    overrides_applied: dict[str, Any]

    def model_dump(self, **_: Any) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SlotRemapEvent:
    from_index: int
    to_index: int
    filament_id: str | None = None

    def model_dump(self, **_: Any) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SwapInstruction:
    z: float
    toolhead: int
    from_slot: int
    to_slot: int
    from_colour: str
    to_colour: str
    label: str

    def model_dump(self, **_: Any) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DiffReport:
    source_filename: str
    output_filename: str
    reference_profile: str
    output_printer: str | None = None
    source_nozzle_diameters: list[float] = field(default_factory=list)
    output_nozzle_diameters: list[float] = field(default_factory=list)
    identity_swaps: list[IdentitySwap] = field(default_factory=list)
    gcode_swaps: list[GcodeSwapEvent] = field(default_factory=list)
    keys_dropped: list[KeyDropEvent] = field(default_factory=list)
    values_clamped: list[ClampEvent] = field(default_factory=list)
    rules_matched: list[RuleMatch] = field(default_factory=list)
    slot_remaps: list[SlotRemapEvent] = field(default_factory=list)
    model_keys_dropped: list[KeyDropEvent] = field(default_factory=list)
    slice_artifacts_stripped: list[str] = field(default_factory=list)
    advanced_overrides_applied: dict[str, Any] = field(default_factory=dict)
    swap_instructions: list[SwapInstruction] = field(default_factory=list)
    swap_pauses_skipped_painted: bool = False

    def counts(self) -> dict[str, int]:
        return {
            "identity_swaps": len(self.identity_swaps),
            "gcode_swaps": len(self.gcode_swaps),
            "keys_dropped": len(self.keys_dropped),
            "values_clamped": len(self.values_clamped),
            "rules_matched": len(self.rules_matched),
            "slot_remaps": len(self.slot_remaps),
            "model_keys_dropped": len(self.model_keys_dropped),
            "slice_artifacts_stripped": len(self.slice_artifacts_stripped),
            "advanced_overrides_applied": len(self.advanced_overrides_applied),
            "swap_instructions": len(self.swap_instructions),
        }

    def model_dump(self, *, exclude: set[str] | None = None, **_: Any) -> dict[str, Any]:
        result = asdict(self)
        for key in exclude or ():
            result.pop(key, None)
        return result


@dataclass
class RuleMatchConditions:
    filament_settings_id_contains: str | None = None
    filament_vendor: str | None = None
    filament_type: str | None = None
    base_profile_contains: str | None = None


@dataclass
class RuleDefinition:
    name: str
    description: str = ""
    match: RuleMatchConditions = field(default_factory=RuleMatchConditions)
    overrides: dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    enabled: bool = True
    source_path: str | None = None


@dataclass
class ProfileDescriptor:
    id: str
    display_name: str
    path: str
    source: str
    layer_height: str | None = None
    printer_variant: str | None = None
    nozzle_diameters: list[float] = field(default_factory=list)

    def model_dump(self, *, exclude: set[str] | None = None, **_: Any) -> dict[str, Any]:
        result = asdict(self)
        for key in exclude or ():
            result.pop(key, None)
        return result
