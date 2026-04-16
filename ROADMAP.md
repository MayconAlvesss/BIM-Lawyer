# BIM-Lawyer Revit Plugin Roadmap

## Current Status (MVP Phase)
- **Status:** Functional Foundation.
- **Frontend (C#):** The plugin successfully crawls the entire physical 3D model (Omni-Collector) using highly optimized ActiveView filtering, extracting geometries and variables. The DataGrid UI is styled and interactive.
- **Backend (Python):** The FastAPI server is functional, receiving massive payloads and completing the request/response cycle.
- **Pending/Known Limitations:** The normative engine (math and parameter comparison) currently lacks calibration for native Revit internal units (e.g., Decimal Feet to Meters conversion precision on complex elements) and exact Architectural parameter mappings. Therefore, the plugin is successfully communicating and reading elements, but the true "legal compliance detection" is still undergoing refinement.

---

## The 20 Expansion Ideas for Future Sprints
As brainstormed for creating a highly advanced, professional, and market-ready engineering tool:

1. **Auto-Correção Ativa (Auto-Fixer):** Expand the skeleton to automatically adjust dimensions according to the closest legal parameter globally.
2. **"Raio-X" de Acessibilidade 3D:** Implement transparent materials (Glassmorphism) with glowing neon red edges for failing geometry.
3. **Módulo de Saídas de Emergência:** Pathfinding algorithms to calculate physical distance of escape routes and fire doors.
4. **Exportação de Laudo Legal (PDF):** One-click generation of a technical PDF stamped with the firm's logo to hand to the architect.
5. **Dashboard Web/Mobile:** Allow investors to see the model compliance live through a webpage.
6. **Módulo Construtor de Leis:** Interface inside Revit allowing the user to create custom mathematical rules without programming.
7. **Integração com Navisworks:** Export XML clash reports for legal compliance.
8. **Auditoria de Custo de Multas:** Predict the monetary loss to the owner if the highlighted issues are not resolved.
9. **Módulo Acústico (NBR 15575):** Analyze wall layers to verify sound insulation ratings.
10. **Aviso Sonoro e Chatbot:** Implement an AI that literally talks to the modeler explaining the legal error.
11. **Calculadora Termodinâmica:** Solar radiation rules for window placement.
12. **Detecção de Tubulações Conflitantes:** Check MEP spacing distances (plumbing inside concrete slabs).
13. **Assinatura Digital (Blockchain):** Register the compliance report immutably to protect the engineers politically.
14. **Leitura de Pisos Táteis:** Auto-detect if ramps have correct tactile flooring modeled before and after them.
15. **Auditoria em Real-Time (Live Sync):** Evaluate elements exactly the moment the user clicks "Draw" in Revit.
16. **Validação de Código de Bombeiros Local:** Check sprinkler coverage spheres based on ceilings.
17. **Filtro de Fase de Projeto:** Differentiate between As-Built auditing and Executive Design auditing.
18. **Módulo Gêmeos Digitais (IoT):** Sync actual sensor data of built walls over the BIM logic.
19. **Análise de Ventilação Cruzada:** Vectorial checking between windows of the same physical room.
20. **Gamificação:** Give the modeler an "Accuracy Score" (e.g., 95%) mimicking code quality platforms like SonarQube.
