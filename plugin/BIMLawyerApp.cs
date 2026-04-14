using System;
using System.IO;
using System.Reflection;
using System.Windows.Media.Imaging;
using Autodesk.Revit.UI;

namespace BIMLawyerPlugin
{
    public class BIMLawyerApp : IExternalApplication
    {
        public Result OnStartup(UIControlledApplication application)
        {
            // 1. Create Ribbon Tab
            string tabName = "BIM-Lawyer";
            try { application.CreateRibbonTab(tabName); } catch { }

            // 2. Create Ribbon Panel
            RibbonPanel panel = application.CreateRibbonPanel(tabName, "Audit & Compliance");

            // 3. Create Push Button
            string assemblyPath = Assembly.GetExecutingAssembly().Location;
            PushButtonData buttonData = new PushButtonData(
                "AuditButton",
                "Full Audit",
                assemblyPath,
                "BIMLawyerPlugin.AuditCommand"
            );

            buttonData.ToolTip = "Perform a normative audit on the current project vs International Standards.";
            
            // Note: Icons would be added here if available in resources
            // buttonData.LargeImage = LoadIcon("audit_icon_32x32.png");

            panel.AddItem(buttonData);

            return Result.Succeeded;
        }

        public Result OnShutdown(UIControlledApplication application)
        {
            return Result.Succeeded;
        }

        private BitmapImage LoadIcon(string iconName)
        {
            // Placeholder logic for icon loading from assembly resources
            return null;
        }
    }
}
