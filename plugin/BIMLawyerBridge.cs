using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Http;
using System.Text.Json;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Autodesk.Revit.Attributes;

namespace BIMLawyerPlugin
{
    [Transaction(TransactionMode.Manual)]
    public class AuditCommand : IExternalCommand
    {
        private static readonly HttpClient client = new HttpClient();
        private const string ApiEndpoint = "http://localhost:8000/api/v1/audit/batch";
        private const string ApiKey = "bim-lawyer-secure-key-2026"; // In prod, manage securely

        public Result Execute(
          ExternalCommandData commandData,
          ref string message,
          ElementSet elements)
        {
            UIApplication uiapp = commandData.Application;
            UIDocument uidoc = uiapp.ActiveUIDocument;
            Document doc = uidoc.Document;

            try
            {
                // 1. Collect target elements (Doors, Ramps)
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
                        units = "DECIMAL_FEET", // Native Revit internal units
                        params_ = new { width = width },
                        bounding_box = bbox != null ? new
                        {
                            min = new[] { bbox.Min.X, bbox.Min.Y, bbox.Min.Z },
                            max = new[] { bbox.Max.X, bbox.Max.Y, bbox.Max.Z }
                        } : null
                    });
                }

                var requestBody = new
                {
                    jurisdiction = "ADA", // Could be mapped from UI combobox
                    elements = payloadElements
                };

                // 2. Perform Async REST Request
                string jsonPayload = JsonSerializer.Serialize(requestBody);
                var content = new StringContent(jsonPayload, Encoding.UTF8, "application/json");
                
                client.DefaultRequestHeaders.Clear();
                client.DefaultRequestHeaders.Add("X-API-Key", ApiKey);

                // Note: Blocking call used for demonstration in IExternalCommand context
                HttpResponseMessage response = client.PostAsync(ApiEndpoint, content).Result;
                
                if (response.IsSuccessStatusCode)
                {
                    TaskDialog.Show("BIM-Lawyer Audit", "Audit request sent successfully.\nCheck dashboard for results.");
                    return Result.Succeeded;
                }
                else
                {
                    message = $"API returned error: {response.StatusCode}";
                    return Result.Failed;
                }
            }
            catch (Exception ex)
            {
                message = ex.Message;
                return Result.Failed;
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
    }
}
