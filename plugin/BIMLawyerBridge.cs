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
            try
            {
                // Instantiate the handler and the external event
                AuditRequestHandler handler = new AuditRequestHandler();
                ExternalEvent exEvent = ExternalEvent.Create(handler);

                // Initialize the modern Window and Show it
                BIMLawyerUI uiWindow = new BIMLawyerUI(exEvent, handler);
                uiWindow.Show();

                return Result.Succeeded;
            }
            catch (Exception ex)
            {
                message = ex.Message;
                return Result.Failed;
            }
        }
    }
}
