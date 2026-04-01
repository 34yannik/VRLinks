using System;
using System.Collections.ObjectModel;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows;
using System.Xml.Serialization;

namespace VRLinks
{
    public static class DataManager
    {
        // file path where all data is stored
        public static readonly string SaveFile = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
            "VRLinks", "links.xml");

        /// <summary>
        /// load lists from file, or create default "Favorites"
        /// </summary>
        public static ObservableCollection<LinkList> Load()
        {
            try
            {
                if (File.Exists(SaveFile))
                {
                    XmlSerializer serializer = new XmlSerializer(typeof(List<LinkList>));
                    using (FileStream fs = new FileStream(SaveFile, FileMode.Open))
                    {
                        var loadedLists = (List<LinkList>)serializer.Deserialize(fs);
                        return new ObservableCollection<LinkList>(loadedLists ?? new List<LinkList>());
                    }
                }
                else
                {
                    // create default favorites if no file exists
                    var fav = new LinkList { Name = "Favorites" };
                    fav.Links.Add(new LinkItem("YouTube", "https://youtube.com"));
                    fav.Links.Add(new LinkItem("Twitch", "https://twitch.tv"));
                    fav.Links.Add(new LinkItem("VRChat", "https://vrchat.com"));

                    return new ObservableCollection<LinkList> { fav };
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error loading data: " + ex.Message);
                return new ObservableCollection<LinkList>();
            }
        }

        /// <summary>
        /// save lists to XML file
        /// </summary>
        public static void Save(ObservableCollection<LinkList> lists)
        {
            try
            {
                string dir = Path.GetDirectoryName(SaveFile);
                if (!Directory.Exists(dir))
                    Directory.CreateDirectory(dir);

                // convert ObservableCollection to List for serialization
                var listsToSave = lists.Select(l => new LinkList
                {
                    Name = l.Name,
                    Links = new ObservableCollection<LinkItem>(l.Links)
                }).ToList();

                XmlSerializer serializer = new XmlSerializer(typeof(List<LinkList>));
                using (FileStream fs = new FileStream(SaveFile, FileMode.Create))
                {
                    serializer.Serialize(fs, listsToSave);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error saving data: " + ex.Message);
            }
        }
    }
}