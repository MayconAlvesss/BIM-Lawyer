# <p align="center">BIM-Lawyer</p>

<p align="center">
  <img src="https://img.icons8.com/wired/128/007ACC/scales.png" width="80" />
</p>

> [!IMPORTANT]
> **Project Status: Concept / Scaffold (2028+)**
> This repository is part of Maycon Alves' technical vision for the AEC Tech ecosystem. It is currently in the **concept and initial architecture phase**. Full development and core implementation will resume after the author returns from his mission in **2028**.

---

### ⚖️ Technical Overview
**BIM-Lawyer** is an automated AEC code compliance and normative audit engine. It bridges the gap between static building codes and dynamic BIM geometry by providing real-time verification and AI-driven remediation suggestions.

Designed to mirror the high-fidelity orchestration of **EcoBIM-Logic**, it focuses on cross-jurisdiction legal auditing.

### 🚀 Core Capabilities
- **Multi-Jurisdiction Audit:** Real-time checking against **ADA (USA)**, **IBC (International)**, and **NBR 9050 (Brazil)**.
- **Parametric Rule Engine:** High-performance geometric validation for doors, ramps, stairs, and egress routes.
- **Normative RAG Hybrid:** AI-driven explanation engine that provides the legal basis for every violation detected.
- **Revit Native Bridge:** Seamless integration via C# plugin for automated data extraction and result visualization.

### 🛠️ Tech Stack
- **Backend:** `FastAPI`, `Pydantic`
- **Logic:** `Modular Rule Engine (Python 3.12+)`
- **Intelligence:** `LangChain`, `Gemini AI` (RAG-LLM Hybrid)
- **Plugin:** `C# / Revit API`

---

### 📂 Repository Structure
- `api/`: High-fidelity FastAPI backend and audit endpoints.
- `core/`: Jurisdiction-aware rule engine and data validation schemas.
- `database/`: Structured normative thresholds and context data.
- `llm/`: Normative RAG implementation for code reference lookups.
- `web/`: Cinematic Glassmorphism dashboard for audit reporting.

<p align="center">
  <sub>BIM Developer | AEC Tech Specialist | International Normative Audit</sub>
</p>
