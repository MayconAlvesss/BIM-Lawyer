# BIM-Lawyer | Advanced Normative Audit Engine ⚖️🏛️

![BIM-Lawyer Banner](https://img.icons8.com/wired/128/007ACC/scales.png)

**Automated AEC Code Compliance & AI-Driven Regulatory Remediations for BIM Workflows.**

BIM-Lawyer is a high-performance, production-ready normative auditing system that bridges the gap between complex building codes and 3D geometry. Engineered for feature parity with **EcoBIM-Logic**, it implements an asynchronous pipeline for real-time compliance validation, ensuring architectural data matches jurisdictional laws (ADA, IBC, NBR).

---

## ✅ Status

> **Production Core — Fully operational.** The C# Revit Bridge communicates seamlessly with the FastAPI backend. The Normative Strategy Engine is 100% functional with support for international unit conversion (Decimal Feet to Metric). LangChain RAG integration is online for normative justifications.

---

## 🚀 Key Features

- **Revit Add-in (C# / .NET 8):** A professional bridge that extracts spatial parameters, hierarchy, and metadata directly from the Revit database via `IExternalCommand` and syncs to the backend.
- **Normative Strategy Engine:** Implementations of the **Strategy Pattern** for deterministic validation across multiple jurisdictions (e.g., NBR 9050, ADA Standards).
- **AI-Driven Legal Foundation:** Uses **LangChain RAG** and **ChromaDB** vector retrieval to explain the legal basis for every geometric violation discovered with precise citations.
- **Automated Audit Reports (PDF/JSON):** Generates enterprise-grade compliance summaries using `fpdf2`, featuring KPIs, violation tables, and remediation suggestions.
- **FastAPI REST Infrastructure:** Secure, asynchronous API layer with specialized performance tracking middleware and API Key authentication.
- **Declarative Unit Normalization:** Advanced Pydantic schemas with custom `@validators` that automatically convert native Revit "Decimal Feet" units into Metric validation models.
- **Containerized Environment:** Fully supported via **Docker** and **Docker Compose** for seamless cloud deployment and dependency management.

---

## 🛠️ Technical Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.12, FastAPI, Uvicorn, Pydantic (V2) |
| **BIM Connector** | C#, .NET 8, Revit API 2024, WPF Logic |
| **Intelligence (AI)** | LangChain, OpenAI/Gemini Embeddings, ChromaDB |
| **Reporting** | FPDF2, JSON Serialization |
| **Security** | API Key Auth, Performance Middleware |
| **Infrastructure** | Docker, Docker Compose, Enterprise Logging |

---

## 📂 Project Structure

```text
BIM-Lawyer/
├── plugin/                  # C# Revit Add-in (Modular Source)
│   ├── src/                 # Services, Models, and UI logic
│   ├── BIMLawyer.csproj     # Visual Studio Project
│   └── BIMLawyer.addin      # Revit Manifest
├── api/                     # FastAPI REST API (Enterprise Setup)
│   ├── auth.py              # Security & API Key validation
│   ├── middleware.py        # Performance tracking logic
│   └── main.py              # API Gateway
├── core/                    # Normative & Geometry Processors
│   ├── geometric_utils.py   # Spatial math and unit conversion
│   ├── normative_engine.py  # Audit strategy pattern brain
│   ├── exceptions.py        # Custom AEC exception hierarchy
│   └── schemas.py           # Pydantic V2 data contracts
├── llm/                     # LangChain RAG & AI Integration
├── database/                # Vector store and Normative DBs
├── utils/                   # Shared utilities (Logger, PDF Generator)
├── lab/                     # Integrated Audit simulations & Debug tools
├── docker/                  # Production Dockerfile & Compose
└── requirements.txt         # Comprehensive dependency manifest
```

---

## ⚡ Quick Start

### Prerequisites
- Python **3.12+**
- Visual Studio **2022** (.NET 8 SDK)
- Autodesk Revit **2024**

---

### Step 1 — Python Environment & Backend

```powershell
# Create an isolated enterprise environment
python -m venv venv

# Activate and Install all dependencies
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

### Step 2 — Configuration & API Launch

```powershell
# Launch the API Gateway
# Ensure you have your keys in config/settings.py or .env
uvicorn api.main:app --reload --port 8000
```

---

### Step 3 — Install the Revit Plugin

1. Open `plugin/BIMLawyer.csproj` in Visual Studio.
2. Build the solution in **x64 Debug/Release**.
3. The build event automatically deploys the `.addin` and `.dll` to:
   `%AppData%\Autodesk\Revit\Addins\2024`

---

### Step 4 — Integrated Debug & PDF Report

Run the full system audit simulator to verify logic and generate the compliance documentation:

```powershell
python lab/integrated_audit.py
```
> Outputs will include a full audit summary in the console and a timestamped **PDF Report** in `lab/reports/`.

---

## 🗺️ Roadmap & Next Steps

- [x] **Enterprise Structural Reform:** Multi-tier architectural expansion.
- [x] **PDF Compliance Reporting:** Export audit results as professional documentation.
- [ ] **Real-time Dashboard:** Web UI (React/Vite) for central management of multiple BIM projects.
- [ ] **Write-back integration:** Directly modify Revit parameters (e.g., `BIML_Status`) via the API.
- [ ] **Advanced Fire Safety:** Expand normative rules to egress path calculations.

---

## 📄 License

This enterprise auditor is developed for international code compliance and automated BIM legal auditing.
See internal project docs for detailed licensing and usage terms.

---

<div align="center">
  <b>Developed with high-density architectural logic for complex international AEC workflows.</b>
  <br><br>
  <i>⚖️ Architecture & Engineering by <b>Maycon Alves</b></i>
  <br>
  <a href="https://github.com/MayconAlvesss" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" />
  </a>
  <a href="https://www.linkedin.com/in/mayconalvess/" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
</div>
