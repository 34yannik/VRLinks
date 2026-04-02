# VRLinks

**VRLinks** is a simple WPF desktop app to manage and organize your favorite links. Save, rename, copy, and arrange links into custom lists. All data is stored locally in XML format.  

I built this for fun because I needed a quick way to store some links for VRChat.

---

## Features

- **Multiple Lists** – Create and manage multiple link collections.  
- **Add / Rename / Delete Links** – Inline editing for quick updates.  
- **Copy URL** – Copy links to the clipboard with one click.  
- **Persistent Storage** – Data is automatically saved in XML.  
- **Tags** – Add comma-separated tags to links.
- **YouTube Thumbnail Preview** – For YouTube links, the video thumbnail is automatically displayed in the list.  

---

## Installation

1. Clone or download the repository.  
2. Open the solution in Visual Studio.  
3. Build and run the `VRLinks` project.  

> The app automatically creates a data folder in your AppData directory:  
> `C:\Users\<YourUser>\AppData\Roaming\VRLinks\links.xml`

---

## Usage

1. **Select a list** from the sidebar or create a new one.  
2. **Add a link** by typing a name, URL, and optional tags, then click `Add`.  
3. **Rename a link** using the inline textbox and ✔ button.  
4. **Delete a link** with the `Delete` button.  
5. **Copy a link** by clicking on it in the list.  
6. **Clear all links** from a list with `Clear All`.  
7. **Open the data folder** via the config button at the top-left.  
8. **Filter links** by typing in the search box; searches both names and URLs.  
9. **View YouTube thumbnails** for links pointing to YouTube; the thumbnail appears on the right side of the list item.  

---

## File Structure

- **MainWindow.xaml / MainWindow.xaml.cs** – WPF interface, list rendering, click handling, and YouTube thumbnail integration.  
- **DataManager.cs** – Handles loading and saving XML data. Converts `ObservableCollection` to XML-serializable lists and back.  
- **LinkList.cs / LinkItem.cs** – Classes for link lists and individual links. `LinkItem` now has a constructor and supports `Tags` and optional `ThumbnailUrl`.  

---

## Dependencies

- .NET 6 or higher (WPF)  
- No external libraries required  
- Uses only built-in WPF controls and `HttpClient` for YouTube thumbnail fetching  

---

## Notes

- **Serialization:** `ObservableCollection` cannot be serialized directly. The app uses helper classes to store lists and links as `List<T>` for XML.  
- **YouTube Thumbnails:** The app automatically detects YouTube URLs and builds the thumbnail URL using the standard YouTube format:  
  `https://img.youtube.com/vi/<videoId>/hqdefault.jpg`.  
- **Data Storage:** All data is stored locally in a single XML file. Deleting this file will reset your lists to the default Favorites.  

---

## License

This project is free to use and modify.  
