using System;
using System.Collections.ObjectModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace VRLinks
{
    public partial class MainWindow : Window
    {
        private ObservableCollection<LinkList> Lists; // all link lists
        private LinkList CurrentList; // currently selected list

        public MainWindow()
        {
            InitializeComponent();

            // Load lists from disk or create default "Favorites"
            Lists = DataManager.Load();
            ListsListBox.ItemsSource = Lists;

            if (Lists.Count > 0)
                ListsListBox.SelectedIndex = 0; // select first list
        }

        // when user selects a different list in sidebar
        private void ListsListBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (ListsListBox.SelectedItem is LinkList list)
            {
                CurrentList = list;
                LinksListView.ItemsSource = CurrentList.Links;
            }
        }

        // add a new link
        private void AddButton_Click(object sender, RoutedEventArgs e)
        {
            if (CurrentList == null)
            {
                MessageBox.Show("Please select a list first!");
                return;
            }

            string name = NameTextBox.Text.Trim();
            string url = UrlTextBox.Text.Trim();

            if (name == "Name" || url == "https://" || string.IsNullOrWhiteSpace(name) || string.IsNullOrWhiteSpace(url))
            {
                MessageBox.Show("Enter a valid name and URL!");
                return;
            }

            // check for duplicate link names
            if (CurrentList.Links.Any(l => string.Equals(l.Name, name, StringComparison.OrdinalIgnoreCase)))
            {
                MessageBox.Show("A link with this name already exists!");
                return;
            }

            CurrentList.Links.Add(new LinkItem(name, url));
            DataManager.Save(Lists); // save automatically

            // reset input boxes
            NameTextBox.Text = "Name";
            NameTextBox.Foreground = Brushes.Gray;

            UrlTextBox.Text = "https://";
            UrlTextBox.Foreground = Brushes.Gray;
        }

        // clear all links in current list
        private void ClearButton_Click(object sender, RoutedEventArgs e)
        {
            if (CurrentList == null) return;

            if (MessageBox.Show("Delete all links?", "Warning", MessageBoxButton.YesNo) == MessageBoxResult.Yes)
            {
                CurrentList.Links.Clear();
                DataManager.Save(Lists); // save after clearing
            }
        }

        // copy link URL to clipboard
        private void CopyButton_Click(object sender, RoutedEventArgs e)
        {
            if (sender is Button btn && btn.DataContext is LinkItem link)
            {
                Clipboard.SetText(link.Url);
            }
        }

        // delete a link
        private void DeleteButton_Click(object sender, RoutedEventArgs e)
        {
            if (CurrentList == null) return;

            if (sender is Button btn && btn.DataContext is LinkItem link)
            {
                CurrentList.Links.Remove(link);
                DataManager.Save(Lists); // save after deletion
            }
        }

        // rename a link (binding auto-updates UI)
        private void RenameButton_Click(object sender, RoutedEventArgs e)
        {
            LinksListView.Items.Refresh();
            DataManager.Save(Lists); // save changes
        }

        // add a new list
        private void AddList_Click(object sender, RoutedEventArgs e)
        {
            string name = ShowInputDialog("Enter new list name:", "New List");
            if (string.IsNullOrWhiteSpace(name)) return;

            if (Lists.Any(l => string.Equals(l.Name, name, StringComparison.OrdinalIgnoreCase)))
            {
                MessageBox.Show("A list with this name already exists!");
                return;
            }

            var newList = new LinkList { Name = name };
            Lists.Add(newList);
            ListsListBox.SelectedItem = newList;
            DataManager.Save(Lists); // save after adding
        }

        // handle placeholder text for TextBoxes
        private void TextBox_GotFocus(object sender, RoutedEventArgs e)
        {
            if (sender is TextBox tb && tb.Foreground == Brushes.Gray)
            {
                tb.Text = "";
                tb.Foreground = Brushes.White;
            }
        }

        private void TextBox_LostFocus(object sender, RoutedEventArgs e)
        {
            if (sender is TextBox tb && string.IsNullOrWhiteSpace(tb.Text))
            {
                if (tb.Name == "NameTextBox") tb.Text = "Name";
                else if (tb.Name == "UrlTextBox") tb.Text = "https://";
                tb.Foreground = Brushes.Gray;
            }
        }

        // open the folder where all data is saved
        private void ConfigButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                string folder = System.IO.Path.GetDirectoryName(DataManager.SaveFile);
                if (!System.IO.Directory.Exists(folder))
                    System.IO.Directory.CreateDirectory(folder);

                System.Diagnostics.Process.Start(new System.Diagnostics.ProcessStartInfo()
                {
                    FileName = folder,
                    UseShellExecute = true,
                    Verb = "open"
                });
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error opening folder: " + ex.Message);
            }
        }

        // simple input dialog for new list names
        private string ShowInputDialog(string text, string defaultText = "")
        {
            Window inputWindow = new Window
            {
                Width = 300,
                Height = 120,
                Title = text,
                WindowStartupLocation = WindowStartupLocation.CenterOwner,
                ResizeMode = ResizeMode.NoResize,
                Background = new SolidColorBrush(Color.FromRgb(30, 30, 30)),
                Owner = this
            };

            var sp = new StackPanel { Margin = new Thickness(10) };
            var tb = new TextBox
            {
                Text = defaultText,
                Foreground = Brushes.White,
                Background = new SolidColorBrush(Color.FromRgb(46, 46, 46)),
                BorderThickness = new Thickness(1),
                Padding = new Thickness(4)
            };
            sp.Children.Add(tb);

            var buttons = new StackPanel { Orientation = Orientation.Horizontal, HorizontalAlignment = HorizontalAlignment.Right, Margin = new Thickness(0, 10, 0, 0) };
            var ok = new Button { Content = "OK", Width = 60, Margin = new Thickness(0, 0, 5, 0) };
            var cancel = new Button { Content = "Cancel", Width = 60 };
            buttons.Children.Add(ok);
            buttons.Children.Add(cancel);
            sp.Children.Add(buttons);

            inputWindow.Content = sp;

            string result = null;
            ok.Click += (s, e) => { result = tb.Text; inputWindow.DialogResult = true; inputWindow.Close(); };
            cancel.Click += (s, e) => { inputWindow.DialogResult = false; inputWindow.Close(); };

            inputWindow.ShowDialog();
            return result;
        }
    }
}