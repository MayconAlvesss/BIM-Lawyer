from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .schemas import BIMElement, AuditResult, Jurisdiction
from .geometric_utils import GeometricEngine
import json
import os
import logging

logger = logging.getLogger(__name__)

class ComplianceRule(ABC):
    """ Abstract Strategy class for Normative Audit Rules. """
    
    @abstractmethod
    def evaluate(self, element: BIMElement, jurisdiction: Jurisdiction, context: Dict) -> AuditResult:
        pass

class DoorWidthRule(ComplianceRule):
    def evaluate(self, element: BIMElement, jurisdiction: Jurisdiction, context: Dict) -> AuditResult:
        # Utilize geometric engine if direct parameters fail
        width = element.params.get("width")
        if not width and element.bounding_box:
            width = GeometricEngine.get_clear_width(element.bounding_box)
            
        required = context.get("accessibility", {}).get(jurisdiction.value, {}).get("door_width", 0.80)
        
        status = "Compliant" if width and width >= required else "Non-Compliant"
        return AuditResult(
            element_id=element.id,
            status=status,
            rule_violated="Minimum Door Width" if status == "Non-Compliant" else None,
            current_value=width,
            required_value=required,
            jurisdiction=jurisdiction.value,
            details=f"Evaluated door clearance. Required: {required}m. Extracted: {width}m",
            severity="HIGH" if status == "Non-Compliant" else "INFO"
        )

class RampSlopeRule(ComplianceRule):
    def evaluate(self, element: BIMElement, jurisdiction: Jurisdiction, context: Dict) -> AuditResult:
        slope = element.params.get("slope", 0)
        required = context.get("accessibility", {}).get(jurisdiction.value, {}).get("ramp_slope", 0.0833)
        
        status = "Non-Compliant" if slope > required else "Compliant"
        return AuditResult(
            element_id=element.id,
            status=status,
            rule_violated="Maximum Ramp Slope" if status == "Non-Compliant" else None,
            current_value=slope,
            required_value=required,
            jurisdiction=jurisdiction.value,
            details=f"Evaluated ramp pitch. Max Allowed: {required*100}%. Extracted: {slope*100}%",
            severity="HIGH" if status == "Non-Compliant" else "INFO"
        )

class WindowSillHeightRule(ComplianceRule):
    def evaluate(self, element: BIMElement, jurisdiction: Jurisdiction, context: Dict) -> AuditResult:
        sill_height = element.params.get("sill_height", 0)
        required = context.get("accessibility", {}).get(jurisdiction.value, {}).get("max_window_sill_height", 0.80)
        
        status = "Non-Compliant" if sill_height > required else "Compliant"
        return AuditResult(
            element_id=element.id,
            status=status,
            rule_violated="Maximum Window Sill Height (Visual Access)" if status == "Non-Compliant" else None,
            current_value=sill_height,
            required_value=required,
            jurisdiction=jurisdiction.value,
            details=f"Evaluated window sill. Max Allowed for wheelchair view: {required}m. Extracted: {sill_height}m",
            severity="WARNING" if status == "Non-Compliant" else "INFO"
        )

class SanitaryAccessibilityRule(ComplianceRule):
    def evaluate(self, element: BIMElement, jurisdiction: Jurisdiction, context: Dict) -> AuditResult:
        # Simplified rule: checks if a toilet has the minimum required frontal clearance parameter
        frontal_clearance = element.params.get("frontal_clearance", 0)
        required = context.get("accessibility", {}).get(jurisdiction.value, {}).get("min_toilet_frontal_clearance", 1.20)
        
        status = "Compliant" if frontal_clearance >= required else "Non-Compliant"
        return AuditResult(
            element_id=element.id,
            status=status,
            rule_violated="Minimum Toilet Frontal Clearance" if status == "Non-Compliant" else None,
            current_value=frontal_clearance,
            required_value=required,
            jurisdiction=jurisdiction.value,
            details=f"Evaluated fixture clearance. Required: {required}m. Found: {frontal_clearance}m",
            severity="HIGH" if status == "Non-Compliant" else "INFO"
        )

# PHASE 7: Structural & Civil Architecture Rules
class WallThicknessRule(ComplianceRule):
    def evaluate(self, element: BIMElement, jurisdiction: Jurisdiction, context: Dict) -> AuditResult:
        h = element.params.get("thickness", element.params.get("width", 0))
        if h == 0: return None
        req = 0.10
        status = "Compliant" if h >= req else "Non-Compliant"
        return AuditResult(element_id=element.id, status=status, rule_violated="Min Wall Thickness (0.10m)", current_value=round(h,3), required_value=req, jurisdiction=jurisdiction.value, details="Minimum structural block.", severity="HIGH")

class WallLengthExpansionRule(ComplianceRule):
    def evaluate(self, element: BIMElement, jurisdiction: Jurisdiction, context: Dict) -> AuditResult:
        l = element.params.get("length", 0)
        if l == 0: return None
        req = 15.0
        status = "Compliant" if l <= req else "Non-Compliant"
        return AuditResult(element_id=element.id, status=status, rule_violated="Max Wall Run (15m Expansion Joint)", current_value=round(l,3), required_value=req, jurisdiction=jurisdiction.value, details="Walls longer than 15m crack without joints.", severity="HIGH")

class WallHeightRule(ComplianceRule):
    def evaluate(self, element: BIMElement, jurisdiction: Jurisdiction, context: Dict) -> AuditResult:
        h = element.params.get("unconnected_height", element.params.get("height", 0))
        if h == 0: return None
        req = 4.0
        status = "Compliant" if h <= req else "Non-Compliant"
        return AuditResult(element_id=element.id, status=status, rule_violated="Max Unbraced Wall Height (4m)", current_value=round(h,3), required_value=req, jurisdiction=jurisdiction.value, details="Walls taller need beams.", severity="WARNING")

class StairWidthRule(ComplianceRule):
    def evaluate(self, element: BIMElement, jurisdiction: Jurisdiction, context: Dict) -> AuditResult:
        w = element.params.get("width", 0)
        if w == 0: return None
        req = 1.20
        status = "Compliant" if w >= req else "Non-Compliant"
        return AuditResult(element_id=element.id, status=status, rule_violated="Min Stair Route Width (1.2m)", current_value=round(w,3), required_value=req, jurisdiction=jurisdiction.value, details="Fire Egress limit.", severity="HIGH")

class MinimumCeilingHeightRule(ComplianceRule):
    def evaluate(self, element: BIMElement, jurisdiction: Jurisdiction, context: Dict) -> AuditResult:
        h = element.params.get("height_offset", 0)
        if h == 0: return None
        req = 2.40
        status = "Compliant" if h >= req else "Non-Compliant"
        return AuditResult(element_id=element.id, status=status, rule_violated="Min Habitable Ceiling (2.40m)", current_value=round(h,3), required_value=req, jurisdiction=jurisdiction.value, details="Habitability.", severity="HIGH")

class MinimumDoorHeightRule(ComplianceRule):
    def evaluate(self, element: BIMElement, jurisdiction: Jurisdiction, context: Dict) -> AuditResult:
        h = element.params.get("height", 0)
        if h == 0: return None
        req = 2.10
        status = "Compliant" if h >= req else "Non-Compliant"
        return AuditResult(element_id=element.id, status=status, rule_violated="Min Door Height (2.10m)", current_value=round(h,3), required_value=req, jurisdiction=jurisdiction.value, details="Anthropometric clearance.", severity="HIGH")


class NormativeEngine:
    """ Operations orchestration for the Normative Rules engine using Dependency Injection """
    def __init__(self, norms_path: str = "database/norms_db.json"):
        self.norms_context = self._load_context(norms_path)
        
        # Load Rule Strategies
        self.rules: Dict[str, List[ComplianceRule]] = {
            "DOOR": [DoorWidthRule(), MinimumDoorHeightRule()],
            "RAMP": [RampSlopeRule()],
            "WINDOW": [WindowSillHeightRule()],
            "PLUMBING": [SanitaryAccessibilityRule()],
            "WALL": [WallThicknessRule(), WallLengthExpansionRule(), WallHeightRule()],
            "STAIR": [StairWidthRule()],
            "CEILING": [MinimumCeilingHeightRule()]
        }

    def _load_context(self, path: str):
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        logger.warning("Norms database absent. Mocking baseline context.")
        return {
            "accessibility": {
                "ADA": {"door_width": 0.81, "ramp_slope": 0.083, "corridor_width": 0.92, "max_window_sill_height": 0.91, "min_toilet_frontal_clearance": 1.52},
                "NBR9050": {"door_width": 0.8, "ramp_slope": 0.083, "corridor_width": 1.2, "max_window_sill_height": 0.80, "min_toilet_frontal_clearance": 1.20}
            }
        }

    def audit_element(self, element: BIMElement, jurisdiction: Jurisdiction) -> List[AuditResult]:
        category = element.category.upper()
        results = []
        applied_rules = []
        
        # Map Revit's BuiltInCategories to logic keys
        if "DOOR" in category: applied_rules = self.rules.get("DOOR", [])
        elif "RAMP" in category: applied_rules = self.rules.get("RAMP", [])
        elif "WINDOW" in category: applied_rules = self.rules.get("WINDOW", [])
        elif "PLUMBING" in category or "SANITARY" in category: applied_rules = self.rules.get("PLUMBING", [])
        elif "WALL" in category: applied_rules = self.rules.get("WALL", [])
        elif "STAIR" in category: applied_rules = self.rules.get("STAIR", [])
        elif "CEIL" in category or "ROOF" in category: applied_rules = self.rules.get("CEILING", [])
        
        for rule in applied_rules:
            res = rule.evaluate(element, jurisdiction, self.norms_context)
            if res: # Only append if the rule didn't return None
                results.append(res)
            
        if not results:
            results.append(AuditResult(
                element_id=element.id,
                status="Compliant",
                rule_violated="Generic Evaluation",
                current_value=0,
                required_value=0,
                jurisdiction=jurisdiction.value,
                details=f"Scanned by Omni-Collector. Category: {category}",
                severity="INFO"
            ))
            
        return results

    def batch_audit(self, elements: List[Dict[str, Any]], jurisdiction: Jurisdiction) -> List[AuditResult]:
        aggregated_results = []
        for el_dict in elements:
            try:
                el_obj = BIMElement(**el_dict)
                aggregated_results.extend(self.audit_element(el_obj, jurisdiction))
            except Exception as e:
                logger.error(f"Failed to parse or audit element: {e}")
        return aggregated_results
