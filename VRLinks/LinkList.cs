using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VRLinks
{
    public class LinkList
    {
        public string Name { get; set; }
        public ObservableCollection<LinkItem> Links { get; set; } = new ObservableCollection<LinkItem>();
        public override string ToString() => Name;
    }
}
