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
    public class AuditRequestHandler : IExternalEventHandler
    {
        public string SelectedJurisdiction { get; set; } = "NBR9050";
        public BIMLawyerUI UIWindow { get; set; }

        private static readonly HttpClient client = new HttpClient();
        private const string ApiEndpoint = "http://localhost:8000/api/v1/audit/batch";
        private const string ApiKey = "bim-lawyer-secure-key-2026"; 

        public void Execute(UIApplication uiapp)
        {
            UIDocument uidoc = uiapp.ActiveUIDocument;
            Document doc = uidoc.Document;

            try
            {
                UIWindow?.AppendLog("Collecting doors and ramps from current view...");
                
                var doorCollector = new FilteredElementCollector(doc)
                    .OfCategory(BuiltInCategory.OST_Doors)
                    .WhereElementIsNotElementType()
                    .ToList();

                var rampCollector = new FilteredElementCollector(doc)
                    .OfCategory(BuiltInCategory.OST_Ramps)
                    .WhereElementIsNotElementType()
                    .ToList();

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
                        params_ = new { width = width },
                        bounding_box = bbox != null ? new
                        {
                            min = new[] { bbox.Min.X, bbox.Min.Y, bbox.Min.Z },
                            max = new[] { bbox.Max.X, bbox.Max.Y, bbox.Max.Z }
                        } : null
                    });
                }

                UIWindow?.AppendLog($"Found {payloadElements.Count} elements. Sending to BIM-Lawyer Core...");

                var requestBody = new
                {
                    jurisdiction = SelectedJurisdiction,
                    elements = payloadElements
                };

                string jsonPayload = JsonSerializer.Serialize(requestBody);
                var content = new StringContent(jsonPayload, Encoding.UTF8, "application/json");
                
                client.DefaultRequestHeaders.Clear();
                client.DefaultRequestHeaders.Add("X-API-Key", ApiKey);

                // Make async call
                Task.Run(async () => {
                    try
                    {
                        HttpResponseMessage response = await client.PostAsync(ApiEndpoint, content);
                        if (response.IsSuccessStatusCode)
                        {
                            string resultStr = await response.Content.ReadAsStringAsync();
                            // Very simple string find instead of full parsing for the UI log
                            int compliantCount = resultStr.Split(new string[] { "\"status\":\"Compliant\"" }, StringSplitOptions.None).Length - 1;
                            int total = payloadElements.Count;
                            int nonCompliant = total - compliantCount;
                            
                            UIWindow?.AppendLog($"Success! Audit complete.\n- Elements passed: {compliantCount}\n- Violations found: {nonCompliant}\nCheck your lab/reports folder for the PDF.");
                        }
                        else
                        {
                            UIWindow?.AppendLog($"API returned error: {response.StatusCode}");
                        }
                    }
                    catch (Exception ex)
                    {
                        UIWindow?.AppendLog("Request failed: " + ex.Message);
                    }
                });
            }
            catch (Exception ex)
            {
               UIWindow?.AppendLog("Error during geometry collection: " + ex.Message);
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
