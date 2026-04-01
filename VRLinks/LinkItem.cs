using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VRLinks
{
    public class LinkItem
    {
        public string Name { get; set; }
        public string Url { get; set; }

        public LinkItem() { }

        public LinkItem(string name, string url)
        {
            Name = name;
            Url = url;
        }
    }
}
