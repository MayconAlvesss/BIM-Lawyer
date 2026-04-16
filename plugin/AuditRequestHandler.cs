using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace BIMLawyerPlugin
{
    public class AuditResultData
    {
        public string element_id { get; set; }
        public string status { get; set; }
        public string rule_violated { get; set; }
        public object current_value { get; set; }
        public object required_value { get; set; }
    }

    public class AuditRequestHandler : IExternalEventHandler
    {
        public string SelectedJurisdiction { get; set; } = "NBR9050";
        public BIMLawyerUI UIWindow { get; set; }
        public string ActiveCommand { get; set; }
        public string ActiveSelectedElementId { get; set; }

        private static readonly HttpClient client = new HttpClient();
        private const string ApiEndpoint = "http://localhost:8000/api/v1/audit/batch";
        private const string ApiKey = "bim-lawyer-secure-key-2026"; 

        private List<AuditResultData> _lastResults = new List<AuditResultData>();

        public void Execute(UIApplication uiapp)
        {
            UIDocument uidoc = uiapp.ActiveUIDocument;
            Document doc = uidoc.Document;

            try
            {
                if (ActiveCommand == "CLEAR")
                {
                    ClearOverrides(doc);
                    UIWindow?.BindDataGrid(null);
                    return;
                }
                
                if (ActiveCommand == "ZOOM_TO_ELEMENT")
                {
                    if (!string.IsNullOrEmpty(ActiveSelectedElementId))
                    {
                        var targetEl = doc.GetElement(ActiveSelectedElementId);
                        if (targetEl != null)
                        {
                            uidoc.Selection.SetElementIds(new List<ElementId> { targetEl.Id });
                            uidoc.ShowElements(targetEl.Id); // Revit native Zoom to Element bounds
                        }
                    }
                    UIWindow?.BindDataGrid(_lastResults);
                    return;
                }

                if (ActiveCommand == "AUTO_FIX_ALL" || ActiveCommand == "AUTO_FIX_SELECTED")
                {
                    using (Transaction t = new Transaction(doc, "BIM-Lawyer Auto-Fix Engine"))
                    {
                        t.Start();
                        int fixedCount = 0;
                        var targets = ActiveCommand == "AUTO_FIX_SELECTED" 
                            ? _lastResults.Where(r => r.element_id == ActiveSelectedElementId) 
                            : _lastResults.Where(r => r.status.Contains("Non-Compliant"));

                        foreach (var target in targets)
                        {
                            try {
                                Element el = doc.GetElement(target.element_id);
                                if (el != null && target.required_value != null) {
                                    
                                    string rule = target.rule_violated ?? "";
                                    double reqValFLOAT = Convert.ToDouble(target.required_value.ToString());
                                    
                                    if (rule.Contains("Door Width")) {
                                        Parameter p = el.get_Parameter(BuiltInParameter.DOOR_WIDTH);
                                        if (p != null && !p.IsReadOnly) { p.Set(reqValFLOAT); fixedCount++; target.status = "Compliant"; target.current_value = target.required_value; }
                                    }
                                    else if (rule.Contains("Sill Height")) {
                                        Parameter p = el.get_Parameter(BuiltInParameter.INSTANCE_SILL_HEIGHT_PARAM);
                                        if (p != null && !p.IsReadOnly) { p.Set(reqValFLOAT); fixedCount++; target.status = "Compliant"; target.current_value = target.required_value; }
                                    }
                                }
                            } catch { } // Silent block if parameter isn't instance-writable or type bounds block it.
                        }
                        t.Commit();
                        TaskDialog.Show("Mitigation Engine", $"Action Complete! Successfully adjusted {fixedCount} element(s) automatically.");
                    }
                    UIWindow?.BindDataGrid(_lastResults);
                    ApplyHeatmapColors(doc, _lastResults); // Re-paint to turn them Green
                    return;
                }

                // Data Extraction: Omni-Collector Engine (High Performance View Filter)
                var allElements = new FilteredElementCollector(doc, doc.ActiveView.Id)
                    .WhereElementIsNotElementType()
                    .Where(e => e.Category != null && e.Category.CategoryType == CategoryType.Model)
                    .ToList();

                var payloadElements = new List<object>();

                foreach (var el in allElements)
                {
                    BoundingBoxXYZ bbox = el.get_BoundingBox(null);
                    double? width = GetParameterAsDouble(el, BuiltInParameter.DOOR_WIDTH) ?? GetParameterAsDouble(el, BuiltInParameter.WINDOW_WIDTH) ?? GetParameterAsDouble(el, BuiltInParameter.GENERIC_WIDTH);
                    double? sillHeight = GetParameterAsDouble(el, BuiltInParameter.INSTANCE_SILL_HEIGHT_PARAM);
                    double? height = GetParameterAsDouble(el, BuiltInParameter.DOOR_HEIGHT) ?? GetParameterAsDouble(el, BuiltInParameter.WINDOW_HEIGHT) ?? GetParameterAsDouble(el, BuiltInParameter.GENERIC_HEIGHT);
                    double? thickness = GetParameterAsDouble(el, BuiltInParameter.WALL_BASE_WIDTH) ?? GetParameterAsDouble(el, BuiltInParameter.FLOOR_ATTR_THICKNESS_PARAM) ?? GetParameterAsDouble(el, BuiltInParameter.GENERIC_THICKNESS);
                    double? length = GetParameterAsDouble(el, BuiltInParameter.CURVE_ELEM_LENGTH);
                    double? unconnHeight = GetParameterAsDouble(el, BuiltInParameter.WALL_USER_HEIGHT_PARAM);
                    double? heightOffset = GetParameterAsDouble(el, BuiltInParameter.CEILING_HEIGHTABOVELEVEL_PARAM);
                    double? riserHeight = GetParameterAsDouble(el, BuiltInParameter.STAIRS_ACTUAL_RISER_HEIGHT);
                    double? treadDepth = GetParameterAsDouble(el, BuiltInParameter.STAIRS_ACTUAL_TREAD_DEPTH);
                    
                    double mockFrontalClearance = el.Category.Name.Contains("Plumbing") ? 1.10 : 0; // Mocking bad toilet clearance

                    payloadElements.Add(new
                    {
                        id = el.UniqueId,
                        category = el.Category.Name,
                        units = "DECIMAL_FEET",
                        @params = new { 
                            width = width, 
                            height = height,
                            sill_height = sillHeight, 
                            thickness = thickness,
                            length = length,
                            unconnected_height = unconnHeight,
                            height_offset = heightOffset,
                            riser_height = riserHeight,
                            tread_depth = treadDepth,
                            frontal_clearance = mockFrontalClearance 
                        },
                        bounding_box = bbox != null ? new
                        {
                            min = new[] { bbox.Min.X, bbox.Min.Y, bbox.Min.Z },
                            max = new[] { bbox.Max.X, bbox.Max.Y, bbox.Max.Z }
                        } : null
                    });
                }

                var requestBody = new
                {
                    jurisdiction = SelectedJurisdiction,
                    elements = payloadElements
                };

                string jsonPayload = JsonSerializer.Serialize(requestBody);
                var content = new StringContent(jsonPayload, Encoding.UTF8, "application/json");
                
                client.DefaultRequestHeaders.Clear();
                client.DefaultRequestHeaders.Add("X-API-Key", ApiKey);

                // Synchronous bridge to maintain Revit DB safety envelope
                HttpResponseMessage response = client.PostAsync(ApiEndpoint, content).Result;
                
                if (response.IsSuccessStatusCode)
                {
                    string resultStr = response.Content.ReadAsStringAsync().Result;
                    
                    using (JsonDocument docJson = JsonDocument.Parse(resultStr))
                    {
                        string resultsArray = docJson.RootElement.GetProperty("results").GetRawText();
                        var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                        _lastResults = JsonSerializer.Deserialize<List<AuditResultData>>(resultsArray, options);
                    }
                    
                    UIWindow?.BindDataGrid(_lastResults);
                    ApplyHeatmapColors(doc, _lastResults);
                }
                else
                {
                    TaskDialog.Show("API Error", $"The server responded with an error: {response.StatusCode}\nEnsure the Python Uvicorn server is running correctly.");
                    UIWindow?.BindDataGrid(null);
                }
            }
            catch (Exception ex)
            {
                UIWindow?.BindDataGrid(null);
                TaskDialog.Show("Connection Error", $"Failed to connect to the BIM-Lawyer engine: {ex.Message}\n\nDid you forget to start the Uvicorn terminal as instructed?");
            }
        }

        private void ApplyHeatmapColors(Document doc, List<AuditResultData> results)
        {
            if (results == null || results.Count == 0)
            {
                TaskDialog.Show("Audit Notice", "No legally mapped elements were found or all evaluated elements failed to return data.");
                return;
            }

            using (Transaction t = new Transaction(doc, "BIM-Lawyer Heatmap"))
            {
                t.Start();
                OverrideGraphicSettings greenOptions = new OverrideGraphicSettings();
                greenOptions.SetSurfaceForegroundPatternColor(new Color(0, 255, 0));
                
                var solidPatternId = new FilteredElementCollector(doc).OfClass(typeof(FillPatternElement)).Cast<FillPatternElement>().FirstOrDefault(a => a.GetFillPattern().IsSolidFill)?.Id;
                if(solidPatternId != null) greenOptions.SetSurfaceForegroundPatternId(solidPatternId);

                OverrideGraphicSettings redOptions = new OverrideGraphicSettings();
                redOptions.SetSurfaceForegroundPatternColor(new Color(255, 0, 0));
                if(solidPatternId != null) redOptions.SetSurfaceForegroundPatternId(solidPatternId);

                int colorCount = 0;
                foreach (var r in results)
                {
                    try
                    {
                        Element el = doc.GetElement(r.element_id);
                        if (el != null)
                        {
                            if (r.status.Contains("Compliant") && !r.status.Contains("Non-Compliant"))
                            {
                                doc.ActiveView.SetElementOverrides(el.Id, greenOptions);
                            }
                            else
                            {
                                doc.ActiveView.SetElementOverrides(el.Id, redOptions);
                            }
                            colorCount++;
                        }
                    }
                    catch { } // Ignore graphical override errors on incompatible elements
                }
                t.Commit();
                // TaskDialog.Show("Debug", $"Painted {colorCount} elements out of {results.Count} returned by AI.");
            }
        }

        private void ClearOverrides(Document doc)
        {
            using (Transaction t = new Transaction(doc, "Clear BIM-Lawyer Overrides"))
            {
                t.Start();
                
                var allElements = new FilteredElementCollector(doc, doc.ActiveView.Id)
                    .WhereElementIsNotElementType()
                    .Where(e => e.Category != null && e.Category.CategoryType == CategoryType.Model)
                    .ToList();
                
                OverrideGraphicSettings clearOpts = new OverrideGraphicSettings();
                
                foreach (var el in allElements)
                {
                    try { doc.ActiveView.SetElementOverrides(el.Id, clearOpts); } catch { }
                }
                t.Commit();
            }
        }

        private double? GetParameterAsDouble(Element el, BuiltInParameter param)
        {
            Parameter p = el.get_Parameter(param);
            if (p != null && p.StorageType == StorageType.Double)
            {
                return p.AsDouble();
            }
            return null;
        }

        public string GetName() => "AuditRequestHandler";
    }
}
