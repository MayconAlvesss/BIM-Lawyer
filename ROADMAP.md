# BIM-Lawyer Revit Plugin Roadmap

## Current Status (MVP Phase)
- **Status:** Functional Foundation.
- **Frontend (C#):** The plugin successfully crawls the entire physical 3D model (Omni-Collector) using highly optimized ActiveView filtering, extracting geometries and variables. The DataGrid UI is styled and interactive.
- **Backend (Python):** The FastAPI server is functional, receiving massive payloads and completing the request/response cycle.
- **Pending/Known Limitations:** The normative engine (math and parameter comparison) currently lacks calibration for native Revit internal units (e.g., Decimal Feet to Meters conversion precision on complex elements) and exact Architectural parameter mappings. Therefore, the plugin is successfully communicating and reading elements, but the true "legal compliance detection" is still undergoing refinement.

---

## The 20 Expansion Ideas for Future Sprints
As brainstormed for creating a highly advanced, professional, and market-ready engineering tool:

1. **Active Auto-Fixer:** Expand the skeleton to automatically adjust dimensions according to the closest legal parameter globally.
2. **3D Accessibility X-Ray:** Implement transparent materials (Glassmorphism) with glowing neon red edges for failing geometry.
3. **Emergency Egress Module:** Pathfinding algorithms to calculate physical distance of escape routes and fire doors.
4. **Legal Report PDF Export:** One-click generation of a technical PDF stamped with the firm's logo to hand to the architect.
5. **Web/Mobile Dashboard:** Allow investors to see the model compliance live through a webpage.
6. **Rule Builder Module:** Interface inside Revit allowing the user to create custom mathematical rules without programming.
7. **Navisworks Integration:** Export XML clash reports for legal compliance.
8. **Fine Cost Predictor Audit:** Predict the monetary loss to the owner if the highlighted issues are not resolved.
9. **Acoustic Insulation Module (NBR 15575):** Analyze wall layers to verify sound insulation ratings.
10. **Voice Warning and AI Chatbot:** Implement an AI that literally talks to the modeler explaining the legal error.
11. **Thermodynamic Calculator:** Solar radiation rules for window placement.
12. **Conflicting Pipe Detection:** Check MEP spacing distances (plumbing inside concrete slabs).
13. **Blockchain Digital Signature:** Register the compliance report immutably to protect the engineers politically.
14. **Tactile Flooring Audit:** Auto-detect if ramps have correct tactile flooring modeled before and after them.
15. **Real-Time Live Sync Audit:** Evaluate elements exactly the moment the user clicks "Draw" in Revit.
16. **Local Fire Department Code Validation:** Check sprinkler coverage spheres based on ceilings.
17. **Project Phase Filter:** Differentiate between As-Built auditing and Executive Design auditing.
18. **Digital Twins IoT Module:** Sync actual sensor data of built walls over the BIM logic.
19. **Cross Ventilation Analysis:** Vectorial checking between windows of the same physical room.
20. **Gamification Engine:** Give the modeler an "Accuracy Score" (e.g., 95%) mimicking code quality platforms like SonarQube.
