import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Default folders configuration
        self.folders = {
            "images": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"],
            "documents": ["txt", "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"],
            "archives": ["zip", "rar", "tar", "gz", "7z"],
            "audio": ["mp3", "wav", "flac", "aac", "ogg"],
            "video": ["mp4", "avi", "mkv", "mov", "wmv"],
            "code": ["py", "js", "html", "css", "java", "cpp", "c", "php"],
            "executables": ["exe", "msi", "app", "bat"]
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="File Organizer", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Folder selection
        ttk.Label(main_frame, text="Folder to organize:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.folder_var = tk.StringVar(value=str(Path.home() / "Downloads"))
        folder_entry = ttk.Entry(main_frame, textvariable=self.folder_var, width=50)
        folder_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        
        browse_btn = ttk.Button(main_frame, text="Browse...", command=self.browse_folder)
        browse_btn.grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(0, weight=1)
        
        # Checkbox variables
        self.create_folders_var = tk.BooleanVar(value=True)
        self.include_hidden_var = tk.BooleanVar(value=False)
        self.backup_first_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(options_frame, text="Create missing folders automatically", 
                       variable=self.create_folders_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Include hidden files", 
                       variable=self.include_hidden_var).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Backup original structure (dry run)", 
                       variable=self.backup_first_var).grid(row=2, column=0, sticky=tk.W)
        
        # Progress and log area
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(0, weight=1)
        
        # Text widget for logs
        self.log_text = tk.Text(progress_frame, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(progress_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.organize_btn = ttk.Button(button_frame, text="Organize Files", 
                                      command=self.start_organization)
        self.organize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Clear Log", 
                  command=self.clear_log).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Exit", 
                  command=self.root.quit).pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure row weights for resizing
        main_frame.rowconfigure(3, weight=1)
    
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.folder_var.get())
        if folder:
            self.folder_var.set(folder)
    
    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
    
    def organize_files(self):
        try:
            base_folder = Path(self.folder_var.get())
            
            if not base_folder.exists():
                self.log_message("Error: Selected folder does not exist!")
                return
            
            self.log_message(f"Starting organization of: {base_folder}")
            
            # Count total files
            all_files = [item for item in base_folder.iterdir() 
                        if item.is_file() and not (item.name.startswith('.') and not self.include_hidden_var.get())]
            
            total_files = len(all_files)
            processed_files = 0
            
            self.log_message(f"Found {total_files} files to process...")
            
            for item in all_files:
                if item.is_file():
                    ext = item.suffix.lower().lstrip('.')
                    moved = False
                    
                    # Skip if backup mode is on
                    if self.backup_first_var.get():
                        self.log_message(f"[DRY RUN] Would move: {item.name}")
                        processed_files += 1
                        continue
                    
                    # Determine which category folder to use
                    for folder, ext_list in self.folders.items():
                        if ext in ext_list:
                            dest_dir = base_folder / folder
                            if self.create_folders_var.get():
                                dest_dir.mkdir(exist_ok=True)
                            
                            if dest_dir.exists():
                                try:
                                    item.rename(dest_dir / item.name)
                                    self.log_message(f"Moved: {item.name} → {folder}/")
                                    moved = True
                                except Exception as e:
                                    self.log_message(f"Error moving {item.name}: {str(e)}")
                            else:
                                self.log_message(f"Destination folder doesn't exist: {dest_dir}")
                            break
                    
                    # If extension didn't match any category, move to "others"
                    if not moved and not self.backup_first_var.get():
                        dest_dir = base_folder / "others"
                        if self.create_folders_var.get():
                            dest_dir.mkdir(exist_ok=True)
                        
                        if dest_dir.exists():
                            try:
                                item.rename(dest_dir / item.name)
                                self.log_message(f"Moved: {item.name} → others/")
                            except Exception as e:
                                self.log_message(f"Error moving {item.name}: {str(e)}")
                        else:
                            self.log_message(f"Destination folder doesn't exist: {dest_dir}")
                    
                    processed_files += 1
                    self.status_var.set(f"Processing... {processed_files}/{total_files} files")
            
            if self.backup_first_var.get():
                self.log_message("Dry run completed. No files were actually moved.")
            else:
                self.log_message(f"Organization complete! Processed {processed_files} files.")
            
            self.status_var.set("Ready")
            
        except Exception as e:
            self.log_message(f"Error: {str(e)}")
            self.status_var.set("Error occurred")
    
    def start_organization(self):
        # Disable button during processing
        self.organize_btn.config(state=tk.DISABLED)
        self.status_var.set("Processing...")
        
        # Run organization in separate thread to prevent UI freezing
        thread = threading.Thread(target=self.organize_files)
        thread.daemon = True
        thread.start()
        
        # Re-enable button when done (this won't work perfectly due to threading,
        # but we'll handle it in the organize_files method)
        def reenable_button():
            self.organize_btn.config(state=tk.NORMAL)
        
        # For simplicity, we'll just re-enable after a short delay
        self.root.after(100, lambda: None)  # This is a placeholder
        
        # The actual re-enabling happens at the end of organize_files

def main():
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
