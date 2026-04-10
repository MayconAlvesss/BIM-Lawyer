"""
BIM-Lawyer — IFC Mock Ingestion
===============================
Simulates the extraction of geometric and metadata parameters from an IFC file.
Provides the data source for the RuleEngine to perform compliance checks.
"""

import random
import uuid
from typing import List, Dict, Any

class IFCMockParser:
    """
    Mock parser that simulates data extraction from an IFC model (ISO 16739).
    """
    
    def __init__(self, project_name: str = "Demo Project"):
        self.project_name = project_name

    def get_extracted_elements(self) -> List[Dict[str, Any]]:
        """
        Returns a list of BIM elements with parameters extracted for auditing.
        """
        return [
            {
                "element_id": f"DOOR-{uuid.uuid4().hex[:6]}",
                "category": "IfcDoor",
                "name": "Main Entrance Egress",
                "width_in": 34.0, # Compliant (>32")
                "fire_rating": "2HR",
                "floor": "L1"
            },
            {
                "element_id": f"DOOR-{uuid.uuid4().hex[:6]}",
                "category": "IfcDoor",
                "name": "Storage Closet",
                "width_in": 28.0, # NON-COMPLIANT (<32")
                "fire_rating": "0HR",
                "floor": "L1"
            },
            {
                "element_id": f"RAMP-{uuid.uuid4().hex[:6]}",
                "category": "IfcRamp",
                "name": "South Entrance ADA Ramp",
                "slope_ratio": 0.075, # Compliant (<0.0833)
                "has_handrails": True,
                "floor": "L0"
            },
            {
                "element_id": f"RAMP-{uuid.uuid4().hex[:6]}",
                "category": "IfcRamp",
                "name": "Service Ramp B",
                "slope_ratio": 0.12, # NON-COMPLIANT (>0.0833)
                "has_handrails": False,
                "floor": "B1"
            },
            {
                "element_id": f"STAIR-{uuid.uuid4().hex[:6]}",
                "category": "IfcStair",
                "name": "Fire Exit A",
                "width_in": 48.0, # Compliant (>44")
                "tread_depth_in": 11.0,
                "riser_height_in": 7.0
            }
        ]

    def simulate_ifc_stream(self) -> Dict[str, Any]:
        """Provides a full project capture for a bulk audit."""
        return {
            "project": self.project_name,
            "version": "IFC4",
            "element_count": 5,
            "data": self.get_extracted_elements()
        }
