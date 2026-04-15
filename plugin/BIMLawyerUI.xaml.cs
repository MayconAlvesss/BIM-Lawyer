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
            InvokeHandler("AUDIT");
        }

        private void Clear_Click(object sender, RoutedEventArgs e)
        {
            InvokeHandler("CLEAR");
        }

        private void AutoFix_Click(object sender, RoutedEventArgs e)
        {
            InvokeHandler("AUTO_FIX");
        }

        private void InvokeHandler(string command)
        {
            string juri = "NBR9050";
            if (CmbJurisdiction.SelectedItem != null)
            {
                var content = ((System.Windows.Controls.ComboBoxItem)CmbJurisdiction.SelectedItem).Content.ToString();
                juri = content.Split(' ')[0];
            }

            _handler.SelectedJurisdiction = juri;
            _handler.UIWindow = this;
            _handler.ActiveCommand = command;
            
            BtnAudit.IsEnabled = false;
            BtnClear.IsEnabled = false;
            BtnAutoFix.IsEnabled = false;

            _externalEvent.Raise();
        }

        public void BindDataGrid(System.Collections.IEnumerable data)
        {
            Dispatcher.Invoke(() => {
                GridResults.ItemsSource = data;
                BtnAudit.IsEnabled = true;
                BtnClear.IsEnabled = true;
                BtnAutoFix.IsEnabled = true;
            });
        }
    }
}
