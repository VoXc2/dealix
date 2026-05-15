"""Enterprise tier — 90-day transformation program structure tests."""

from __future__ import annotations

from itertools import pairwise

from auto_client_acquisition.enterprise_os.enterprise_program import (
    PROGRAM_DURATION_DAYS,
    get_program,
    list_phases,
    phase_by_key,
)


def test_program_is_ninety_days() -> None:
    program = get_program()
    assert program.duration_days == 90 == PROGRAM_DURATION_DAYS
    assert program.service_id == "enterprise_ai_operating_system"
    assert program.name_ar.strip() and program.name_en.strip()


def test_program_has_six_phases() -> None:
    phases = get_program().phases
    assert len(phases) == 6
    assert phases is list_phases()


def test_phases_cover_weeks_one_to_twelve_contiguously() -> None:
    phases = list_phases()
    assert phases[0].week_start == 1
    assert phases[-1].week_end == 12
    for prev, nxt in pairwise(phases):
        assert prev.week_start <= prev.week_end
        assert nxt.week_start == prev.week_end + 1


def test_every_phase_has_deliverables_and_gate() -> None:
    for phase in list_phases():
        assert phase.deliverables, phase.key
        assert all(d.strip() for d in phase.deliverables), phase.key
        assert phase.gate_checkpoint.strip(), phase.key
        assert phase.name_ar.strip() and phase.name_en.strip(), phase.key


def test_phase_keys_unique() -> None:
    keys = [p.key for p in list_phases()]
    assert len(keys) == len(set(keys))


def test_phase_by_key_lookup() -> None:
    assert phase_by_key("ai_audit") is not None
    assert phase_by_key("scale_plan") is not None
    assert phase_by_key("nonexistent") is None
