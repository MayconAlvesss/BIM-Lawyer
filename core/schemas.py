from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class Jurisdiction(str, Enum):
    USA = "ADA"
    BRAZIL = "NBR9050"
    INTERNATIONAL = "IBC"

class BIMElement(BaseModel):
    id: str
    category: str
    params: Dict[str, Any]

class AuditResult(BaseModel):
    element_id: str
    status: str # Compliant / Non-Compliant
    rule_violated: Optional[str] = None
    current_value: Any
    required_value: Any
    details: str
    jurisdiction: str

class BatchAuditRequest(BaseModel):
    jurisdiction: Jurisdiction
    elements: List[BIMElement]
