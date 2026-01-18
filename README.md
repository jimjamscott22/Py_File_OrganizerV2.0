# File Organizer 🗂️

A lightweight graphical desktop application that automatically organizes files in a selected directory by file type. Designed to reduce clutter and restore sanity to chaotic folders like **Downloads**.

Built with Python and Tkinter, this tool is extremely fast, it's simple, and dependency‑free.

---

## ✨ Features

- **Intuitive GUI**  
  Simple, cross‑platform interface built with Tkinter

- **Smart File Categorization**
  - Images (`jpg`, `png`, `gif`, `bmp`, `webp`, etc.)
  - Documents (`pdf`, `docx`, `txt`, `xlsx`, etc.)
  - Archives (`zip`, `rar`, `tar`, etc.)
  - Audio (`mp3`, `wav`, etc.)
  - Video (`mp4`, `avi`, `mkv`, etc.)
  - Code (`py`, `js`, `html`, `css`, etc.)
  - Executables (`exe`, `msi`, etc.)

- **Customizable Behavior**
  - Include or exclude hidden files
  - Automatically create missing folders
  - Dry‑run mode to preview changes safely

- **Real‑time Feedback**
  - Progress tracking
  - Detailed logging panel

- **Cross‑Platform**
  - Windows
  - macOS
  - Linux

---

## 🧰 Requirements

- Python **3.6+**
- Tkinter (included with most Python installations)

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/file-organizer.git
cd file-organizer
```

### (Optional) Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
```

No additional dependencies are required.

---

## ▶️ Usage

```bash
python file_organizer.py
```

### Steps

1. Select a directory (defaults to **Downloads**)
2. Configure options:
   - Create missing folders
   - Include hidden files
   - Enable dry‑run mode
3. Click **Organize Files**
4. Monitor progress in the log window
5. Review your newly organized directory

---

## 🔐 Safety Notes

- Always back up important data before organizing files
- Use **dry‑run mode** before committing changes
- Files are **moved**, not copied
- Unknown extensions are placed into an `others` folder

---

## ⚙️ Customization

Modify file categories by editing the `folders` dictionary:

```python
folders = {
    "images": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"],
    "documents": ["txt", "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"],
    # Add more categories here...
}
```

---

## 🛠️ Troubleshooting

### Tkinter Not Installed (Linux)

```bash
sudo apt-get install python3-tk
```

### Permission Errors

- Ensure write permissions to the target directory
- Run as administrator (Windows) or with `sudo` (Linux/macOS)

### Files Not Moving

- Check if files are in use
- Ensure destination folders are writable
- Review error messages in the log window

---

## 🤝 Contributing

Contributions are welcome.

```bash
git checkout -b feature/YourFeature
git commit -m "Add YourFeature"
git push origin feature/YourFeature
```

Open a Pull Request when ready.

---

## 📄 License

MIT License.  
See the `LICENSE` file for details.

---

## 🙌 Acknowledgments

- Built entirely with Python’s standard library
- Inspired by real‑world desktop clutter
MIT License — see `LICENSE`.
