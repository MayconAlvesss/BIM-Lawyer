using System;
using System.Windows;
using System.Windows.Input;
using Autodesk.Revit.UI;

namespace BIMLawyerPlugin
{
    public partial class BIMLawyerUI : Window
    {
        private ExternalEvent _externalEvent;
        private AuditRequestHandler _handler;

        public BIMLawyerUI(ExternalEvent exEvent, AuditRequestHandler handler)
        {
            InitializeComponent();
            _externalEvent = exEvent;
            _handler = handler;
        }

        private void TopBar_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            if (e.ChangedButton == MouseButton.Left)
                DragMove();
        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }

        private void Audit_Click(object sender, RoutedEventArgs e)
        {
            string juri = "NBR9050";
            if (CmbJurisdiction.SelectedItem != null)
            {
                var content = ((System.Windows.Controls.ComboBoxItem)CmbJurisdiction.SelectedItem).Content.ToString();
                juri = content.Split(' ')[0]; // Extract "NBR9050" from "NBR9050 (Brazil)"
            }

            _handler.SelectedJurisdiction = juri;
            _handler.UIWindow = this;
            
            TxtLog.Text = $"[{DateTime.Now.ToShortTimeString()}] Dispatching job to BIM-Lawyer engine ({juri})...\nWaiting for Revit API Access...";
            BtnAudit.IsEnabled = false;

            _externalEvent.Raise();
        }

        public void AppendLog(string message)
        {
            Dispatcher.Invoke(() => {
                TxtLog.AppendText("\n[" + DateTime.Now.ToShortTimeString() + "] " + message);
                TxtLog.ScrollToEnd();
                BtnAudit.IsEnabled = true;
            });
        }
    }
}
