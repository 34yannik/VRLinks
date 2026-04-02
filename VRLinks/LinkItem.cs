using System;
using System.Collections.ObjectModel;
using System.ComponentModel;

namespace VRLinks
{
    public class LinkItem : INotifyPropertyChanged
    {
        public string Name { get; set; }
        public string Url { get; set; }
        public ObservableCollection<string> Tags { get; set; }

        private string thumbnailUrl;
        public string ThumbnailUrl
        {
            get => thumbnailUrl;
            set { thumbnailUrl = value; OnPropertyChanged(nameof(ThumbnailUrl)); }
        }

        public LinkItem(string name, string url, ObservableCollection<string> tags = null)
        {
            Name = name;
            Url = url;
            Tags = tags ?? new ObservableCollection<string>();
            UpdateThumbnail();
        }

        private void UpdateThumbnail()
        {
            string videoId = GetYouTubeVideoId(Url);
            if (!string.IsNullOrEmpty(videoId))
                ThumbnailUrl = $"https://img.youtube.com/vi/{videoId}/hqdefault.jpg";
            else
                ThumbnailUrl = null;
        }

        private string GetYouTubeVideoId(string url)
        {
            if (string.IsNullOrWhiteSpace(url)) return null;

            try
            {
                var uri = new Uri(url);

                if (uri.Host.Contains("youtu.be"))
                    return uri.AbsolutePath.TrimStart('/');

                if (uri.Host.Contains("youtube.com"))
                {
                    string query = uri.Query.TrimStart('?');
                    foreach (var part in query.Split('&'))
                    {
                        var kv = part.Split('=');
                        if (kv.Length == 2 && kv[0] == "v")
                            return kv[1];
                    }
                }
            }
            catch { return null; }

            return null;
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged(string prop) =>
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(prop));
    }
}