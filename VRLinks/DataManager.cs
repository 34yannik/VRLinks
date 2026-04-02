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
        public static readonly string SaveFile = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
            "VRLinks", "links.xml");

        public static ObservableCollection<LinkList> Load()
        {
            try
            {
                if (File.Exists(SaveFile))
                {
                    XmlSerializer serializer = new XmlSerializer(typeof(List<SerializableLinkList>));
                    using (FileStream fs = new FileStream(SaveFile, FileMode.Open))
                    {
                        var loaded = (List<SerializableLinkList>)serializer.Deserialize(fs);

                        // Convert to ObservableCollection<LinkList>
                        var obsLists = new ObservableCollection<LinkList>();
                        foreach (var sl in loaded)
                        {
                            var list = new LinkList { Name = sl.Name };
                            foreach (var li in sl.Links)
                            {
                                var link = new LinkItem(li.Name, li.Url);
                                foreach (var tag in li.Tags ?? new List<string>())
                                    link.Tags.Add(tag);
                                list.Links.Add(link);
                            }
                            obsLists.Add(list);
                        }

                        return obsLists;
                    }
                }
                else
                {
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

        public static void Save(ObservableCollection<LinkList> lists)
        {
            try
            {
                string dir = Path.GetDirectoryName(SaveFile);
                if (!Directory.Exists(dir))
                    Directory.CreateDirectory(dir);

                // Convert to serializable type
                var serializableLists = lists.Select(l => new SerializableLinkList
                {
                    Name = l.Name,
                    Links = l.Links.Select(li => new SerializableLinkItem
                    {
                        Name = li.Name,
                        Url = li.Url,
                        Tags = li.Tags.ToList()
                    }).ToList()
                }).ToList();

                XmlSerializer serializer = new XmlSerializer(typeof(List<SerializableLinkList>));
                using (FileStream fs = new FileStream(SaveFile, FileMode.Create))
                {
                    serializer.Serialize(fs, serializableLists);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error saving data: " + ex.Message);
            }
        }

        #region Serializable Helper Classes

        [Serializable]
        public class SerializableLinkList
        {
            public string Name { get; set; }
            public List<SerializableLinkItem> Links { get; set; } = new List<SerializableLinkItem>();
        }

        [Serializable]
        public class SerializableLinkItem
        {
            public string Name { get; set; }
            public string Url { get; set; }
            public List<string> Tags { get; set; } = new List<string>();
        }

        #endregion
    }
}