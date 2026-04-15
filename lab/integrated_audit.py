import time
import os
import json
from core.schemas import BIMElement, Jurisdiction, RevitUnits
from core.rule_engine import NormativeEngine
from utils.report_generator import ComplianceReportGenerator
from utils.logger import logger

def run_debug_audit():
    """
    Simulation script to debug the entire enterprise pipeline.
    Generates the requested PDF and JSON reports for verification.
    """
    logger.info("Starting Integrated Debug Audit...")
    
    # 1. Mock Revit Data (Raw Decimal Feet)
    mock_payload = [
        {
            "id": "REVIT-WALL-001",
            "category": "OST_Doors",
            "units": RevitUnits.DECIMAL_FEET,
            "params": {"width": 2.5}, # 2.5 ft is approx 0.76m (Fails NBR 0.80m)
            "bounding_box": {"min": [0,0,0], "max": [2.5, 0.5, 7.0]}
        },
        {
            "id": "REVIT-RAMP-002",
            "category": "OST_Ramps",
            "units": RevitUnits.DECIMAL_FEET,
            "params": {"slope": 0.05}, # 5% is compliant (Max 8.33%)
            "bounding_box": {"min": [0,0,0], "max": [20, 5, 1]}
        }
    ]

    # 2. Execute Audit Logic
    engine = NormativeEngine()
    jurisdiction = Jurisdiction.BRAZIL # NBR 9050
    
    logger.info(f"Auditing {len(mock_payload)} elements against {jurisdiction.value}...")
    results = engine.batch_audit(mock_payload, jurisdiction)
    
    # 3. Generate Reports
    reporter = ComplianceReportGenerator()
    
    logger.info("Generating Audit Documentation...")
    json_path = reporter.generate_json([r.dict() for r in results], jurisdiction.value)
    pdf_path = reporter.generate_pdf([r.dict() for r in results], jurisdiction.value)
    
    logger.info(f"Debug Complete.")
    logger.info(f"JSON Report: {json_path}")
    logger.info(f"PDF/Text Report: {pdf_path}")
    
    # Output summary to console for immediate debug view
    print("\n--- AUDIT DEBUG SUMMARY ---")
    for res in results:
        print(f"Element: {res.element_id} | Status: {res.status} | Details: {res.details}")
    print("---------------------------\n")

if __name__ == "__main__":
    run_debug_audit()
