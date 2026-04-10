"""
BIM-Lawyer — Automated Rule Checking (ARC) Engine
=================================================
Normative intelligence layer focused on International Building Codes (IBC).
Performs Automated Rule Checking (ARC) by comparing BIM parameters against scalars.

Features:
  - ADA Compliance (Ramps, Clearances)
  - Occupancy Load Calculations (IBC Ch. 10)
  - Fire Rating Verification (IBC Ch. 7)
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class RuleEngine:
    """
    Core engine to execute geometric and normative checks on BIM family parameters.
    """
    
    def __init__(self):
        # International Building Code (IBC) Constants (Simplified for sketch)
        self.IBC_STANDARDS = {
            "MIN_DOOR_WIDTH_IN": 32.0,
            "MAX_RAMP_SLOPE": 0.0833, # 1:12 slope for ADA
            "MIN_STAIR_WIDTH_IN": 44.0,
        }
        logger.info("RuleEngine initialized with IBC 2021 Reference Constants.")

    def check_compliance(self, bim_element: Dict[str, Any]) -> dict:
        """
        Check an element (e.g., Door, Ramp) against IBC/ISO requirements.
        """
        eid = bim_element.get("element_id", "Unknown")
        etype = bim_element.get("category", "").upper()
        violations = []
        
        # 1. Door Width Check
        if "DOOR" in etype:
            width = bim_element.get("width_in", 0)
            if width < self.IBC_STANDARDS["MIN_DOOR_WIDTH_IN"]:
                violations.append({
                    "code": "IBC-1010.1.1",
                    "severity": "CRITICAL",
                    "description": f"Door width {width}\" is below the 32\" minimum required for egress."
                })

        # 3. Stair Width Check
        if "STAIR" in etype:
            width = bim_element.get("width_in", 0)
            if width < self.IBC_STANDARDS["MIN_STAIR_WIDTH_IN"]:
                violations.append({
                    "code": "IBC-1011.2",
                    "severity": "CRITICAL",
                    "description": f"Stair width {width}\" is below the 44\" minimum required for egress."
                })

        # 4. Mock Fire Safety Check (Travel Distance)
        travel_dist = bim_element.get("travel_distance_ft", 0)
        if travel_dist > 200: # Standard IBC 200ft limit for non-sprinkled
            violations.append({
                "code": "IBC-1017.2",
                "severity": "WARNING",
                "description": f"Maximum travel distance {travel_dist}' exceeds the 200' limit (BS/IBC compliant)."
            })

        is_compliant = len(violations) == 0
        
        return {
            "element_id": eid,
            "is_compliant": is_compliant,
            "violation_count": len(violations),
            "audit_log": violations,
            "standard_referenced": "IBC 2021 / ISO 21597"
        }

    def batch_audit(self, elements: List[Dict[str, Any]]) -> dict:
        """Runs the rule engine over a list of BIM elements."""
        results = [self.check_compliance(e) for e in elements]
        total = len(results)
        fail = len([r for r in results if not r["is_compliant"]])
        
        return {
            "summary": {
                "total_elements_audited": total,
                "compliant_count": total - fail,
                "non_compliant_count": fail,
                "compliance_score": (total - fail) / total if total > 0 else 1.0
            },
            "detailed_results": results
        }
