"""
tests/test_rule_engine.py
Deterministic regression suite for the BIM-Lawyer NormativeEngine (ADA / NBR 9050).

Run from project root:
    pytest tests/ -v
"""
import sys
import os
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from core.rule_engine import (
    NormativeEngine,
    DoorWidthRule,
    RampSlopeRule,
    WallThicknessRule,
    WallLengthExpansionRule,
    StairWidthRule,
    MinimumCeilingHeightRule,
)
from core.schemas import BIMElement, Jurisdiction, RevitUnits


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def engine():
    """Engine with mocked context — no norms_db.json required in CI."""
    return NormativeEngine(norms_path="nonexistent_path_to_force_mock.json")


def make_element(category: str, **params) -> BIMElement:
    """Helper: build a BIMElement with units=METERS so the validator skips unit conversion."""
    return BIMElement(
        id=f"TEST-{category}-001",
        category=category,
        units=RevitUnits.METERS,
        params=params,
        bounding_box=None,
    )


def _mock_context() -> dict:
    """Mirrors the hardcoded fallback context inside NormativeEngine._load_context."""
    return {
        "accessibility": {
            "ADA": {
                "door_width": 0.81,
                "ramp_slope": 0.083,
                "max_window_sill_height": 0.91,
                "min_toilet_frontal_clearance": 1.52,
            },
            "NBR9050": {
                "door_width": 0.80,
                "ramp_slope": 0.083,
                "max_window_sill_height": 0.80,
                "min_toilet_frontal_clearance": 1.20,
            },
        }
    }


# ---------------------------------------------------------------------------
# Group 1 — Door Width  (ADA: 0.81m | NBR9050: 0.80m)
# ---------------------------------------------------------------------------

class TestDoorWidth:

    def test_compliant_door_ada(self):
        rule = DoorWidthRule()
        el = make_element("DOOR", width=0.90)
        result = rule.evaluate(el, Jurisdiction.USA, _mock_context())
        assert result.status == "Compliant"

    def test_non_compliant_door_ada(self):
        rule = DoorWidthRule()
        el = make_element("DOOR", width=0.75)
        result = rule.evaluate(el, Jurisdiction.USA, _mock_context())
        assert result.status == "Non-Compliant"
        assert result.rule_violated == "Minimum Door Width"
        assert result.severity == "HIGH"

    def test_compliant_door_nbr(self):
        rule = DoorWidthRule()
        el = make_element("DOOR", width=0.80)
        result = rule.evaluate(el, Jurisdiction.BRAZIL, _mock_context())
        assert result.status == "Compliant"

    def test_exact_minimum_is_compliant_boundary(self):
        """Boundary: value exactly equal to required must pass (>= check)."""
        rule = DoorWidthRule()
        el = make_element("DOOR", width=0.80)
        result = rule.evaluate(el, Jurisdiction.BRAZIL, _mock_context())
        assert result.status == "Compliant"


# ---------------------------------------------------------------------------
# Group 2 — Ramp Slope  (max 1:12 ≈ 0.083)
# ---------------------------------------------------------------------------

class TestRampSlope:

    def test_gentle_ramp_compliant(self):
        rule = RampSlopeRule()
        el = make_element("RAMP", slope=0.05)
        result = rule.evaluate(el, Jurisdiction.USA, _mock_context())
        assert result.status == "Compliant"

    def test_steep_ramp_non_compliant(self):
        rule = RampSlopeRule()
        el = make_element("RAMP", slope=0.15)
        result = rule.evaluate(el, Jurisdiction.USA, _mock_context())
        assert result.status == "Non-Compliant"
        assert result.severity == "HIGH"

    def test_ramp_at_exact_limit_is_compliant(self):
        rule = RampSlopeRule()
        el = make_element("RAMP", slope=0.083)
        result = rule.evaluate(el, Jurisdiction.BRAZIL, _mock_context())
        assert result.status == "Compliant"


# ---------------------------------------------------------------------------
# Group 3 — Wall Rules
# ---------------------------------------------------------------------------

class TestWallRules:

    def test_thin_wall_non_compliant(self):
        rule = WallThicknessRule()
        el = make_element("WALL", thickness=0.08)
        result = rule.evaluate(el, Jurisdiction.BRAZIL, _mock_context())
        assert result.status == "Non-Compliant"

    def test_standard_wall_compliant(self):
        rule = WallThicknessRule()
        el = make_element("WALL", thickness=0.14)
        result = rule.evaluate(el, Jurisdiction.BRAZIL, _mock_context())
        assert result.status == "Compliant"

    def test_long_wall_needs_expansion_joint(self):
        rule = WallLengthExpansionRule()
        el = make_element("WALL", length=20.0)
        result = rule.evaluate(el, Jurisdiction.BRAZIL, _mock_context())
        assert result.status == "Non-Compliant"
        assert "15m" in result.rule_violated

    def test_short_wall_no_joint_needed(self):
        rule = WallLengthExpansionRule()
        el = make_element("WALL", length=10.0)
        result = rule.evaluate(el, Jurisdiction.BRAZIL, _mock_context())
        assert result.status == "Compliant"

    def test_wall_zero_thickness_returns_none(self):
        """Revit elements with no geometry should not crash the engine."""
        rule = WallThicknessRule()
        el = make_element("WALL", thickness=0)
        result = rule.evaluate(el, Jurisdiction.USA, _mock_context())
        assert result is None


# ---------------------------------------------------------------------------
# Group 4 — Stair Width
# ---------------------------------------------------------------------------

class TestStairWidth:

    def test_narrow_stair_non_compliant(self):
        rule = StairWidthRule()
        el = make_element("STAIR", width=0.90)
        result = rule.evaluate(el, Jurisdiction.USA, _mock_context())
        assert result.status == "Non-Compliant"

    def test_adequate_stair_compliant(self):
        rule = StairWidthRule()
        el = make_element("STAIR", width=1.50)
        result = rule.evaluate(el, Jurisdiction.USA, _mock_context())
        assert result.status == "Compliant"


# ---------------------------------------------------------------------------
# Group 5 — Ceiling Height
# ---------------------------------------------------------------------------

class TestCeilingHeight:

    def test_low_ceiling_non_compliant(self):
        rule = MinimumCeilingHeightRule()
        el = make_element("CEILING", height_offset=2.10)
        result = rule.evaluate(el, Jurisdiction.BRAZIL, _mock_context())
        assert result.status == "Non-Compliant"

    def test_standard_ceiling_compliant(self):
        rule = MinimumCeilingHeightRule()
        el = make_element("CEILING", height_offset=2.60)
        result = rule.evaluate(el, Jurisdiction.BRAZIL, _mock_context())
        assert result.status == "Compliant"


# ---------------------------------------------------------------------------
# Group 6 — NormativeEngine orchestration
# ---------------------------------------------------------------------------

class TestNormativeEngine:

    def test_engine_dispatches_door_rules(self, engine):
        el = make_element("DOOR", width=0.70, height=2.20)
        results = engine.audit_element(el, Jurisdiction.USA)
        assert len(results) >= 1
        assert "Non-Compliant" in [r.status for r in results]

    def test_engine_compliant_door_passes_all(self, engine):
        el = make_element("DOOR", width=0.90, height=2.20)
        results = engine.audit_element(el, Jurisdiction.USA)
        assert all(r.status == "Compliant" for r in results)

    def test_engine_unknown_category_returns_generic_fallback(self, engine):
        el = make_element("FURNITURE", width=1.0)
        results = engine.audit_element(el, Jurisdiction.USA)
        assert len(results) == 1
        assert results[0].rule_violated == "Generic Evaluation"

    def test_batch_audit_processes_multiple_elements(self, engine):
        elements = [
            {"id": "D1", "category": "DOOR", "units": RevitUnits.METERS, "params": {"width": 0.70, "height": 2.20}},
            {"id": "W1", "category": "WALL", "units": RevitUnits.METERS, "params": {"thickness": 0.15, "length": 10.0}},
        ]
        results = engine.batch_audit(elements, Jurisdiction.BRAZIL)
        assert len(results) >= 2

    def test_batch_audit_skips_malformed_without_crashing(self, engine):
        """A malformed dict must not crash the entire batch — batch_audit has try/except."""
        elements = [
            {"id": "GOOD", "category": "DOOR", "units": RevitUnits.METERS, "params": {"width": 0.90, "height": 2.20}},
            {"MISSING_FIELDS": True},  # will be caught by the except block
        ]
        results = engine.batch_audit(elements, Jurisdiction.USA)
        assert len(results) >= 1
