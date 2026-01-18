# File Organizer (Tkinter)

Graphical desktop app that declutters a directory by moving files into categorized folders (images, documents, archives, audio, video, code, executables, others).

## Features
- Simple Tkinter UI with log output and status updates
- Automatic folder creation per category
- Dry-run (preview) mode to see what would move
- Optional inclusion of hidden files
- Cross-platform: Windows, macOS, Linux

## Requirements
- Python 3.6 or higher
- Tkinter (bundled with most Python installs)
- No external packages required

## Setup
```bash
git clone https://github.com/yourusername/file-organizer.git
cd file-organizer
```

### (Optional) Create a virtual environment
Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
macOS/Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```

## Run
```bash
python file_organizer_v2.py
```

## How to use
1) Select the folder to organize (defaults to your Downloads).
2) Choose options:
   - Create missing folders automatically
   - Include hidden files
   - Dry-run (preview only; no files moved)
3) Click **Organize Files**.
4) Watch progress and logs in the window; review results in the destination folder.

## Customization
Edit `folders` in `file_organizer_v2.py` to change categories/extensions:
```python
folders = {
    "images": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"],
    "documents": ["txt", "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"],
    # add more categories here...
}
```
Unknown extensions go to the `others` folder.

## Safety tips
- Use Dry-run first to preview actions.
- Back up important data before organizing.
- The app moves files (does not copy).

## Troubleshooting
- Tkinter missing on some Linux distros: `sudo apt-get install python3-tk`
- Permission errors: ensure write access or run with elevated privileges.
- Files not moving: make sure files aren’t open/locked and destination isn’t read-only.

## License
MIT License — see `LICENSE`.
