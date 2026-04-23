
API_URL = "http://localhost:8000"

def run_simulated_audit():
    print("--- BIM-Lawyer Revit Audit Simulator ---")

    # Mock data as if extracted from Revit (Metric Units)
    elements = [
        {"id": "REV-101", "category": "OST_Doors", "params": {"width": 0.70, "thickness": 0.05}}, # Violates ADA/NBR
        {"id": "REV-102", "category": "OST_Doors", "params": {"width": 0.90, "thickness": 0.05}}, # Compliant
        {"id": "REV-505", "category": "OST_Ramps", "params": {"slope": 0.12}},                   # Steep (Violates)
        {"id": "REV-202", "category": "OST_Corridors", "params": {"width": 1.10}}               # Violates NBR, passes ADA
    ]

    for jid in ["ADA", "NBR9050"]:
        print(f"\n[AUDIT] Starting Batch Audit for Jurisdiction: {jid}")
        payload = {
            "jurisdiction": jid,
            "elements": elements
        }

        try:
            # Note: Server must be running locally for this to work
            # print(f"POST {API_URL}/audit/batch")
            # r = requests.post(f"{API_URL}/audit/batch", json=payload)
            # results = r.json()

            # Simulation of local logic for demonstration
            # from core.rule_engine import NormativeEngine
            # from core.schemas import Jurisdiction
            # engine = NormativeEngine()
            # results = engine.batch_audit(elements, Jurisdiction(jid))

            print(f"Results for {jid}:")
            for el in elements:
                status = "FAILED" if el['id'] in ["REV-101", "REV-505"] or (jid == "NBR9050" and el['id'] == "REV-202") else "PASSED"
                print(f"  - Element {el['id']} ({el['category']}): {status}")

        except Exception as e:
            print(f"  [ERROR] Connection failed: {e}")

if __name__ == "__main__":
    run_simulated_audit()
