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
                
                if (ActiveCommand == "AUTO_FIX")
                {
                    // Placeholder skeleton for mitigation system
                    TaskDialog.Show("Auto-Fix Engine", "Auto-fix routines will be compiled in the next sprint.");
                    UIWindow?.BindDataGrid(_lastResults);
                    return;
                }

                // Data Extraction
                var doorCollector = new FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToList();
                var rampCollector = new FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Ramps).WhereElementIsNotElementType().ToList();

                var payloadElements = new List<object>();

                foreach (var el in doorCollector.Concat(rampCollector))
                {
                    BoundingBoxXYZ bbox = el.get_BoundingBox(null);
                    double? width = GetParameterAsDouble(el, BuiltInParameter.DOOR_WIDTH);

                    payloadElements.Add(new
                    {
                        id = el.UniqueId,
                        category = el.Category.Name,
                        units = "DECIMAL_FEET",
                        @params = new { width = width },
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
                    var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                    _lastResults = JsonSerializer.Deserialize<List<AuditResultData>>(resultStr, options);
                    
                    UIWindow?.BindDataGrid(_lastResults);
                    ApplyHeatmapColors(doc, _lastResults);
                }
            }
            catch (Exception ex)
            {
                UIWindow?.BindDataGrid(null);
            }
        }

        private void ApplyHeatmapColors(Document doc, List<AuditResultData> results)
        {
            using (Transaction t = new Transaction(doc, "BIM-Lawyer Heatmap"))
            {
                t.Start();
                OverrideGraphicSettings greenOptions = new OverrideGraphicSettings();
                greenOptions.SetSurfaceForegroundPatternColor(new Color(0, 255, 0));
                // Get built-in solid pattern
                var solidPatternId = new FilteredElementCollector(doc).OfClass(typeof(FillPatternElement)).Cast<FillPatternElement>().FirstOrDefault(a => a.GetFillPattern().IsSolidFill)?.Id;
                if(solidPatternId != null) greenOptions.SetSurfaceForegroundPatternId(solidPatternId);

                OverrideGraphicSettings redOptions = new OverrideGraphicSettings();
                redOptions.SetSurfaceForegroundPatternColor(new Color(255, 0, 0));
                if(solidPatternId != null) redOptions.SetSurfaceForegroundPatternId(solidPatternId);

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
                        }
                    }
                    catch { } // Ignore graphical override errors on incompatible elements
                }
                t.Commit();
            }
        }

        private void ClearOverrides(Document doc)
        {
            using (Transaction t = new Transaction(doc, "Clear BIM-Lawyer Overrides"))
            {
                t.Start();
                var doorCollector = new FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToList();
                var rampCollector = new FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Ramps).WhereElementIsNotElementType().ToList();
                
                OverrideGraphicSettings clearOpts = new OverrideGraphicSettings();
                
                foreach (var el in doorCollector.Concat(rampCollector))
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
