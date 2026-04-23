import json
import os
from datetime import datetime
from typing import List, Dict, Any

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

class ComplianceReportGenerator:
    """
    Enterprise-grade PDF and JSON report generator for BIM-Lawyer audits.
    Satisfies the client's requirement for a professional audit summary.
    """
    def __init__(self, output_dir: str = "lab/reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_json(self, results: List[Dict[str, Any]], jurisdiction: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audit_{jurisdiction}_{timestamp}.json"
        path = os.path.join(self.output_dir, filename)

        with open(path, "w") as f:
            json.dump({
                "report_metadata": {
                    "jurisdiction": jurisdiction,
                    "generated_at": str(datetime.now()),
                    "tool": "BIM-Lawyer Enterprise 2.0"
                },
                "audit_summary": {
                    "total_elements": len(results),
                    "compliant": len([r for r in results if r.get("status") == "Compliant"]),
                    "non_compliant": len([r for r in results if r.get("status") != "Compliant"])
                },
                "results": results
            }, f, indent=4)
        return path

    def generate_pdf(self, results: List[Dict[str, Any]], jurisdiction: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"compliance_report_{jurisdiction}_{timestamp}.pdf"
        path = os.path.join(self.output_dir, filename)

        if not FPDF_AVAILABLE:
            # Fallback for systems without fpdf - simple txt report
            path = path.replace(".pdf", ".txt")
            with open(path, "w") as f:
                f.write(f"BIM-Lawyer Compliance Report\n{'='*30}\n")
                f.write(f"Jurisdiction: {jurisdiction}\n")
                f.write(f"Generated: {datetime.now()}\n\n")
                for r in results:
                    f.write(f"Element: {r.get('element_id')} | Status: {r.get('status')}\n")
            return path

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, "BIM-Lawyer Compliance Audit Report", ln=True, align="C")

        pdf.set_font("Arial", "", 12)
        pdf.ln(10)
        pdf.cell(190, 10, f"Jurisdiction: {jurisdiction}", ln=True)
        pdf.cell(190, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

        pdf.ln(10)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(60, 10, "Element ID", border=1)
        pdf.cell(40, 10, "Status", border=1)
        pdf.cell(90, 10, "Violation", border=1)
        pdf.ln()

        pdf.set_font("Arial", "", 10)
        for r in results:
            pdf.cell(60, 10, str(r.get("element_id")), border=1)
            pdf.cell(40, 10, str(r.get("status")), border=1)
            pdf.cell(90, 10, str(r.get("rule_violated") or "None"), border=1)
            pdf.ln()

        pdf.output(path)
        return path
