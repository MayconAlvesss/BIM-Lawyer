import json
import os
from typing import List, Dict, Any
from .schemas import BIMElement, AuditResult, Jurisdiction

class NormativeEngine:
    def __init__(self, norms_path: str = "database/norms_db.json"):
        # In a real scenario, this would load from the relative path in the repo
        # For simulation, we'll hardcode or look for the file
        self.norms = {}
        if os.path.exists(norms_path):
            with open(norms_path, "r") as f:
                self.norms = json.load(f)
        else:
            # Fallback for initialization
            self.norms = {
                "accessibility": {
                    "ADA": {"door_width": 0.81, "ramp_slope": 0.083, "corridor_width": 0.92},
                    "NBR9050": {"door_width": 0.8, "ramp_slope": 0.083, "corridor_width": 1.2}
                }
            }

    def audit_element(self, element: BIMElement, jurisdiction: Jurisdiction) -> AuditResult:
        category = element.category.upper()
        params = element.params
        jid = jurisdiction.value
        
        # Default result
        result = AuditResult(
            element_id=element.id,
            status="Compliant",
            current_value=None,
            required_value=None,
            details="Element meets normative requirements.",
            jurisdiction=jid
        )

        if "DOOR" in category:
            width = params.get("width", 0)
            required = self.norms["accessibility"][jid]["door_width"]
            if width < required:
                result.status = "Non-Compliant"
                result.rule_violated = "Minimum Door Width"
                result.current_value = width
                result.required_value = required
                result.details = f"Door too narrow. {jid} requires at least {required}m."

        elif "RAMP" in category:
            slope = params.get("slope", 0)
            required = self.norms["accessibility"][jid]["ramp_slope"]
            if slope > required:
                result.status = "Non-Compliant"
                result.rule_violated = "Maximum Ramp Slope"
                result.current_value = slope
                result.required_value = required
                result.details = f"Ramp is too steep ({slope*100}%). {jid} allows max {required*100}%."

        elif "CORRIDOR" in category or "CIRCULATION" in category:
            width = params.get("width", 0)
            required = self.norms["accessibility"][jid]["corridor_width"]
            if width < required:
                result.status = "Non-Compliant"
                result.rule_violated = "Minimum Corridor Width"
                result.current_value = width
                result.required_value = required
                result.details = f"Corridor below minimum width for accessibility. Required: {required}m."

        return result

    def batch_audit(self, elements: List[Dict[str, Any]], jurisdiction: Jurisdiction) -> List[AuditResult]:
        results = []
        for el_data in elements:
            try:
                element = BIMElement(**el_data)
                results.append(self.audit_element(element, jurisdiction))
            except Exception as e:
                # Log error or add error result
                continue
        return results
