import os
import json
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("780x720")
        self.root.resizable(True, True)
        self.accent_color = "#4f8ef7"
        self.theme = "light"
        self.config_path = Path(__file__).with_name("folders_config.json")
        self.default_folders = {
            "images": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"],
            "documents": ["txt", "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"],
            "archives": ["zip", "rar", "tar", "gz", "7z"],
            "audio": ["mp3", "wav", "flac", "aac", "ogg"],
            "video": ["mp4", "avi", "mkv", "mov", "wmv"],
            "code": ["py", "js", "html", "css", "java", "cpp", "c", "php"],
            "executables": ["exe", "msi", "app", "bat"]
        }
        self.folders = self.load_folders_config()
        
        self.apply_style()
        self.setup_ui()
        self.apply_theme(self.theme)
        
    def _normalize_extensions(self, extensions):
        cleaned = []
        seen = set()
        for ext in extensions:
            if not isinstance(ext, str):
                continue
            norm = ext.strip().lstrip('.').lower()
            if not norm or norm in seen:
                continue
            seen.add(norm)
            cleaned.append(norm)
        return cleaned

    def load_folders_config(self):
        if self.config_path.exists():
            try:
                with self.config_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    cleaned = {}
                    for name, exts in data.items():
                        if not isinstance(name, str) or not isinstance(exts, list):
                            continue
                        cleaned[name] = self._normalize_extensions(exts)
                    if cleaned:
                        return cleaned
            except Exception:
                # Fall back to defaults on any load issue
                pass
        return dict(self.default_folders)

    def save_folders_config(self):
        try:
            payload = {name: sorted(exts) for name, exts in self.folders.items()}
            with self.config_path.open("w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            self.log_message("Saved categories to folders_config.json")
        except Exception as e:
            self.log_message(f"Could not save config: {e}")
    
    def apply_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Accent.TButton", foreground="white", font=("Segoe UI", 10, "bold"))

    def apply_theme(self, theme):
        self.theme = theme
        is_dark = theme == "dark"
        self.bg_color = "#0f172a" if is_dark else "#f5f7fb"
        self.card_bg = "#111827" if is_dark else "white"
        self.text_color = "#e5e7eb" if is_dark else "#1f2933"
        self.muted_text = "#cbd5f5" if is_dark else "#0f172a"
        self.log_bg = "#0b1220" if is_dark else "#f8fafc"
        self.border_color = "#1f2a44" if is_dark else "#e5e9f2"
        button_active = "#3b76d6" if not is_dark else "#2563eb"
        button_disabled = "#a7c4f2" if not is_dark else "#334155"
        accent = "#4f8ef7" if not is_dark else "#60a5fa"
        self.accent_color = accent

        self.root.configure(bg=self.bg_color)
        style = ttk.Style()
        style.configure("Main.TFrame", background=self.bg_color)
        style.configure("Card.TLabelframe", background=self.card_bg, relief="solid", borderwidth=1)
        style.configure("Card.TLabelframe.Label", background=self.card_bg, foreground=self.text_color, font=("Segoe UI", 10, "bold"))
        style.configure("Section.TLabel", background=self.bg_color, foreground=self.muted_text, font=("Segoe UI", 16, "bold"))
        style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 10))
        style.configure("TCheckbutton", background=self.bg_color, foreground=self.text_color)
        style.configure("Accent.TButton", background=accent, foreground="white", font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton",
                  background=[("active", button_active), ("disabled", button_disabled)],
                  foreground=[("disabled", "#e2e8f0")])
        style.configure("TButton", background=self.card_bg, foreground=self.text_color)
        style.configure("Accent.Horizontal.TProgressbar",
                        troughcolor=self.border_color,
                        background=accent,
                        bordercolor=self.border_color,
                        lightcolor=accent,
                        darkcolor=accent)
        style.configure("TEntry", fieldbackground=self.card_bg, foreground=self.text_color)

        if hasattr(self, "log_text"):
            self.log_text.configure(bg=self.log_bg, fg=self.text_color, highlightbackground=self.border_color, insertbackground=self.text_color)
        if hasattr(self, "categories_listbox"):
            self.categories_listbox.configure(bg=self.card_bg, fg=self.text_color, selectbackground=accent, selectforeground="white")
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="16 14 16 16", style="Main.TFrame")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Form variables
        self.category_var = tk.StringVar()
        self.extensions_var = tk.StringVar()
        
        # Title
        title_label = ttk.Label(main_frame, text="File Organizer", style="Section.TLabel")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 14), sticky=tk.W)
        
        # Folder selection
        ttk.Label(main_frame, text="Folder to organize:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.folder_var = tk.StringVar(value=str(Path.home() / "Downloads"))
        folder_entry = ttk.Entry(main_frame, textvariable=self.folder_var, width=50)
        folder_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        
        browse_btn = ttk.Button(main_frame, text="Browse...", command=self.browse_folder)
        browse_btn.grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="12", style="Card.TLabelframe")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(0, weight=1)
        
        # Checkbox variables
        self.create_folders_var = tk.BooleanVar(value=True)
        self.include_hidden_var = tk.BooleanVar(value=False)
        self.backup_first_var = tk.BooleanVar(value=False)
        self.dark_mode_var = tk.BooleanVar(value=self.theme == "dark")
        
        ttk.Checkbutton(options_frame, text="Create missing folders automatically", 
                       variable=self.create_folders_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Include hidden files", 
                       variable=self.include_hidden_var).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Preview (no changes)", 
                       variable=self.backup_first_var).grid(row=2, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Dark mode", 
                       variable=self.dark_mode_var, command=self.toggle_theme).grid(row=3, column=0, sticky=tk.W)
        
        # Categories frame
        categories_frame = ttk.LabelFrame(main_frame, text="Categories", padding="12", style="Card.TLabelframe")
        categories_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        categories_frame.columnconfigure(0, weight=1)
        categories_frame.columnconfigure(1, weight=1)
        categories_frame.columnconfigure(2, weight=1)
        categories_frame.rowconfigure(0, weight=1)
        
        listbox_frame = ttk.Frame(categories_frame)
        listbox_frame.grid(row=0, column=0, rowspan=3, sticky=(tk.N, tk.S, tk.E, tk.W), padx=(0, 10))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)

        self.categories_listbox = tk.Listbox(listbox_frame, height=8, exportselection=False)
        self.categories_listbox.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        cat_scroll = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.categories_listbox.yview)
        cat_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.categories_listbox.configure(yscrollcommand=cat_scroll.set)
        self.categories_listbox.bind("<<ListboxSelect>>", self.on_category_select)

        ttk.Label(categories_frame, text="Category name").grid(row=0, column=1, sticky=tk.W)
        category_entry = ttk.Entry(categories_frame, textvariable=self.category_var)
        category_entry.grid(row=0, column=2, sticky=(tk.W, tk.E))

        ttk.Label(categories_frame, text="Extensions (comma-separated)").grid(row=1, column=1, sticky=tk.W, pady=(6, 0))
        ext_entry = ttk.Entry(categories_frame, textvariable=self.extensions_var)
        ext_entry.grid(row=1, column=2, sticky=(tk.W, tk.E))

        cat_buttons = ttk.Frame(categories_frame)
        cat_buttons.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=(8, 0))
        ttk.Button(cat_buttons, text="Add/Update", command=self.add_or_update_category, style="Accent.TButton").pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(cat_buttons, text="Delete", command=self.delete_category).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(cat_buttons, text="Restore defaults", command=self.restore_default_categories).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(cat_buttons, text="Save", command=self.save_folders_config).pack(side=tk.LEFT)

        # Progress and log area
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="12", style="Card.TLabelframe")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(0, weight=1)
        
        # Text widget for logs
        self.log_text = tk.Text(progress_frame, height=15, wrap=tk.WORD, relief=tk.FLAT, highlightthickness=1)
        scrollbar = ttk.Scrollbar(progress_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100, style="Accent.Horizontal.TProgressbar")
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(8, 0))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame, style="Main.TFrame")
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        self.organize_btn = ttk.Button(button_frame, text="Organize Files", 
                                      command=self.start_organization, style="Accent.TButton")
        self.organize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Clear Log", 
                  command=self.clear_log).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Exit", 
                  command=self.root.quit).pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure row weights for resizing
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        self.refresh_category_list()
    
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.folder_var.get())
        if folder:
            self.folder_var.set(folder)
    
    def log_message(self, message):
        def append():
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)
        self.root.after(0, append)

    def set_status(self, message):
        self.root.after(0, lambda: self.status_var.set(message))

    def update_progress(self, processed, total):
        if total <= 0:
            self.root.after(0, lambda: self.progress_var.set(0))
            return
        percent = min(100, (processed / total) * 100)
        self.root.after(0, lambda: self.progress_var.set(percent))
    
    def toggle_theme(self):
        theme = "dark" if self.dark_mode_var.get() else "light"
        self.apply_theme(theme)

    def refresh_category_list(self):
        self.categories_listbox.delete(0, tk.END)
        for name in sorted(self.folders.keys()):
            self.categories_listbox.insert(tk.END, name)
        if self.folders:
            self.categories_listbox.selection_set(0)
            self.on_category_select()

    def select_category(self, name):
        items = list(self.categories_listbox.get(0, tk.END))
        if name in items:
            idx = items.index(name)
            self.categories_listbox.selection_clear(0, tk.END)
            self.categories_listbox.selection_set(idx)
            self.categories_listbox.see(idx)
            self.on_category_select()

    def on_category_select(self, event=None):
        selection = self.categories_listbox.curselection()
        if not selection:
            self.category_var.set("")
            self.extensions_var.set("")
            return
        name = self.categories_listbox.get(selection[0])
        self.category_var.set(name)
        exts = self.folders.get(name, [])
        self.extensions_var.set(", ".join(exts))

    def add_or_update_category(self):
        name = self.category_var.get().strip()
        if not name:
            self.log_message("Category name cannot be empty.")
            return
        exts = self._normalize_extensions(self.extensions_var.get().split(","))
        if not exts:
            self.log_message("Provide at least one extension.")
            return
        self.folders[name] = exts
        self.refresh_category_list()
        self.select_category(name)
        self.log_message(f"Saved category '{name}' with {len(exts)} extensions.")
        self.save_folders_config()

    def delete_category(self):
        selection = self.categories_listbox.curselection()
        if not selection:
            self.log_message("No category selected to delete.")
            return
        name = self.categories_listbox.get(selection[0])
        if name in self.folders:
            del self.folders[name]
            self.refresh_category_list()
            self.log_message(f"Deleted category '{name}'.")
            self.save_folders_config()

    def restore_default_categories(self):
        self.folders = dict(self.default_folders)
        self.refresh_category_list()
        self.save_folders_config()
        self.log_message("Restored default categories.")

    def _unique_destination(self, dest_dir: Path, original_name: str) -> Path:
        target = dest_dir / original_name
        if not target.exists():
            return target
        stem = Path(original_name).stem
        suffix = Path(original_name).suffix
        counter = 1
        while True:
            candidate = dest_dir / f"{stem} ({counter}){suffix}"
            if not candidate.exists():
                return candidate
            counter += 1
    
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
    
    def organize_files(self):
        try:
            base_folder = Path(self.folder_var.get())
            
            if not base_folder.exists():
                self.log_message("Error: Selected folder does not exist!")
                self.set_status("Error occurred")
                return
            
            self.log_message(f"Starting organization of: {base_folder}")
            
            # Count total files
            all_files = [item for item in base_folder.iterdir() 
                        if item.is_file() and not (item.name.startswith('.') and not self.include_hidden_var.get())]
            
            total_files = len(all_files)
            processed_files = 0
            
            if total_files == 0:
                self.log_message("No files to process.")
                self.set_status("Ready")
                self.update_progress(0, 1)
                return

            self.log_message(f"Found {total_files} files to process...")
            self.update_progress(0, total_files)
            
            for item in all_files:
                if item.is_file():
                    ext = item.suffix.lower().lstrip('.')
                    moved = False
                    
                    # Determine which category folder to use
                    for folder, ext_list in self.folders.items():
                        if ext in ext_list:
                            dest_dir = base_folder / folder
                            if self.create_folders_var.get():
                                dest_dir.mkdir(exist_ok=True)
                            
                            if dest_dir.exists():
                                target_path = self._unique_destination(dest_dir, item.name)
                                if self.backup_first_var.get():
                                    self.log_message(f"[PREVIEW] {item.name} → {target_path.relative_to(base_folder)}")
                                    moved = True
                                else:
                                    try:
                                        item.rename(target_path)
                                        self.log_message(f"Moved: {item.name} → {target_path.relative_to(base_folder)}")
                                        moved = True
                                    except Exception as e:
                                        self.log_message(f"Error moving {item.name}: {str(e)}")
                                        moved = True
                            else:
                                self.log_message(f"Destination folder doesn't exist: {dest_dir}")
                            break
                    
                    # If extension didn't match any category, move to "others"
                    if not moved:
                        dest_dir = base_folder / "others"
                        if self.create_folders_var.get():
                            dest_dir.mkdir(exist_ok=True)
                        
                        if dest_dir.exists():
                            target_path = self._unique_destination(dest_dir, item.name)
                            if self.backup_first_var.get():
                                self.log_message(f"[PREVIEW] {item.name} → {target_path.relative_to(base_folder)}")
                            else:
                                try:
                                    item.rename(target_path)
                                    self.log_message(f"Moved: {item.name} → {target_path.relative_to(base_folder)}")
                                except Exception as e:
                                    self.log_message(f"Error moving {item.name}: {str(e)}")
                        else:
                            self.log_message(f"Destination folder doesn't exist: {dest_dir}")
                    
                    processed_files += 1
                    self.update_progress(processed_files, total_files)
                    self.set_status(f"Processing... {processed_files}/{total_files} files")
            
            if self.backup_first_var.get():
                self.log_message("Preview complete. No files were moved.")
                self.set_status("Preview complete")
            else:
                self.log_message(f"Organization complete! Processed {processed_files} files.")
                self.set_status("Ready")
            
        except Exception as e:
            self.log_message(f"Error: {str(e)}")
            self.set_status("Error occurred")
    
    def start_organization(self):
        # Disable button during processing
        self.organize_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.set_status("Processing...")
        
        # Run organization in separate thread to prevent UI freezing
        thread = threading.Thread(target=self._run_organization_worker)
        thread.daemon = True
        thread.start()

    def _run_organization_worker(self):
        self.organize_files()
        self.root.after(0, self.on_organization_complete)

    def on_organization_complete(self):
        self.organize_btn.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
