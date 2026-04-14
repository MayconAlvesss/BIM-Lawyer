# <p align="center">BIM-Lawyer | Enterprise AEC Auditor</p>

<p align="center">
  <img src="https://img.icons8.com/wired/128/007ACC/scales.png" width="80" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Production%20Core-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/C%23-Revit%20API-purple?style=for-the-badge&logo=c-sharp" />
  <img src="https://img.shields.io/badge/LangChain-RAG-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/ChromaDB-Vector-FE7A36?style=for-the-badge" />
</p>

---

### ⚖️ Enterprise Architectural Overview
**BIM-Lawyer** is a high-fidelity, automated AEC code compliance and normative audit engine. It bridges the gap between static building codes and dynamic BIM geometry by providing real-time verification and AI-driven remediation suggestions.

Engineered with the same technical density as the **EcoBIM-Logic** platform, BIM-Lawyer utilizes an object-oriented Strategy Pattern for deterministic compliance routing, coupled with native Revit unit auto-conversion logic.

### 🚀 Core Technologies & Capabilities
- **C# Revit Addin Context:** Extracts raw spatial arrays and hierarchical parameters directly from the Revit database via `IExternalCommand`.
- **Computational Geometry Engine:** Converts native decimal feet into metric validation models and extracts planar dimensions from 3D Bounding Boxes.
- **LangChain RAG Architecture:** Employs ChromaDB vector store mappings and LLM Embeddings to accurately cite and explain the legal basis for geometric non-compliance.

---

### 🛠️ Quick Start: Revit Plugin Deployment

To see the plugin in Revit, follow these steps:

1. **Build the Solution:**
   - Open `plugin/BIMLawyer.csproj` in Visual Studio 2022.
   - Restore NuGet packages (System.Text.Json).
   - Build in **x64** mode.
2. **Installation:**
   - The build process is configured to automatically copy `BIMLawyer.dll` and `BIMLawyer.addin` to your `%AppData%\Autodesk\Revit\Addins\2024` folder.
3. **Launch Revit:**
   - A new Ribbon Tab **"BIM-Lawyer"** will appear.
   - Click **"Full Audit"** to scan the model and send data to the backend API.

---

### 📂 Structural Blueprint
- `plugin/`: C# .NET environment for native Autodesk Revit injection and data serialization.
- `api/`: Async endpoints, API-key middleware, and standard routing.
- `core/`: The validation brain—features `geometric_utils.py` for spatial computations and `normative_engine.py`.
- `llm/`: `normative_rag.py` implementation mapping text-embeddings via `RetrievalQA` chains.
- `web/`: Cinematic Glassmorphism dashboard logic for presentation.

<p align="center">
  <sub>BIM Developer | AEC Tech Specialist | International Normative Audit</sub>
</p>
