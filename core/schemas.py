from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum

class Jurisdiction(str, Enum):
    USA = "ADA"
    BRAZIL = "NBR9050"
    INTERNATIONAL = "IBC"

class RevitUnits(str, Enum):
    DECIMAL_FEET = "DECIMAL_FEET"
    METERS = "METERS"
    MILLIMETERS = "MILLIMETERS"

class BIMElement(BaseModel):
    id: str = Field(..., description="Unique Element ID from Revit.")
    category: str = Field(..., description="Revit BuiltInCategory, e.g., OST_Doors.")
    units: RevitUnits = Field(default=RevitUnits.DECIMAL_FEET, description="Original unit coordinate system.")
    params: Dict[str, Any] = Field(..., description="Extracted instance parameters.")
    bounding_box: Optional[Dict[str, List[float]]] = Field(
        None,
        description="Min and Max coordinates of the element's bounding box [x, y, z]."
    )

    @validator("params")
    def convert_params_to_metric(cls, v, values):
        """
        Enterprise-grade validator: Automatically converts spatial parameters
        to standard metric (meters) regardless of Revit's internal unit settings.
        """
        unit = values.get('units')
        if unit == RevitUnits.DECIMAL_FEET:
            conversion_factor = 0.3048
            # Only convert dimensional fields
            for key in ["width", "height", "thickness", "clearance"]:
                if key in v and isinstance(v[key], (int, float)):
                    v[key] = v[key] * conversion_factor
        elif unit == RevitUnits.MILLIMETERS:
            conversion_factor = 0.001
            for key in ["width", "height", "thickness", "clearance"]:
                if key in v and isinstance(v[key], (int, float)):
                    v[key] = v[key] * conversion_factor
        return v

class AuditResult(BaseModel):
    element_id: str
    status: str
    rule_violated: Optional[str] = None
    current_value: Any
    required_value: Any
    details: str
    jurisdiction: str
    severity: str = Field(default="WARNING", description="HIGH, WARNING, INFO")

class BatchAuditRequest(BaseModel):
    jurisdiction: Jurisdiction
    elements: List[BIMElement]
