# VRLinks

**VRLinks** is a simple WPF desktop app to manage and organize your favorite links. Save, rename, copy, and arrange links into custom lists. All data is stored locally in XML format.  

I built this for fun because I needed a quick way to store some links for VRChat.

---

## Features

- **Multiple Lists** – Create and manage multiple link collections.  
- **Add / Rename / Delete Links** – Inline editing for quick updates.  
- **Copy URL** – Copy links to the clipboard with one click.  
- **Clear All** – Remove all links from a list easily.  
- **Config Button** – Open the folder where your data is stored.  
- **Persistent Storage** – Data is automatically saved in XML.  
- **Default Favorites** – Preloaded with YouTube, Twitch, and VRChat links.

---

## Screenshots

Here are some screenshots of the app in action:

### Main Window

![Main Window](images/main-window.png)

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
2. **Add a link** by typing a name and URL, then click `Add`.  
3. **Rename a link** using the inline textbox and ✔ button.  
4. **Delete a link** with the `Delete` button.  
5. **Copy a link** using the `Copy` button.  
6. **Clear all links** from a list with `Clear All`.  
7. **Open the data folder** via the config button at the top-left.

---

## File Structure

- **MainWindow.xaml / MainWindow.xaml.cs** – WPF interface and app logic.  
- **DataManager.cs** – Handles loading and saving XML data.  
- **LinkList.cs / LinkItem.cs** – Classes for link lists and individual links.  

---

## Dependencies

- .NET 6 or higher (WPF)  
- No external libraries required  

---

## License

This project is free to use and modify. 
