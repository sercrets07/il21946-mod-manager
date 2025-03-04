import tkinter as tk
from screens.manager import read
import requests
import shutil

class Down_Loader(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ✅ Configure layout
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(1, weight=1)

        # ✅ Label for the Listbox
        self.label = tk.Label(self, text="Available Mods:", font=("Arial", 12))
        self.label.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=5)

        # ✅ Create the Listbox
        self.listbox = tk.Listbox(self, height=20, width=25, yscrollcommand=lambda *args: scrollbar.set(*args))
        self.listbox.grid(row=1, column=0, sticky="ns", padx=(20, 0), pady=5)

        # ✅ Scrollbar
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=1, column=1, sticky="ns", padx=(0, 10), pady=5)

        # ✅ Load mod names from JSON
        self.mods = read()
        for mod in self.mods:
            self.listbox.insert(tk.END, mod["name"])

        # ✅ Create ModDownloader instance
        self.downloader = ModDownloader(self.listbox, self.mods)

        # ✅ Ensure the listbox and scrollbar are linked
        self.listbox.config(yscrollcommand=scrollbar.set)

        # ✅ Download Button (Top Button)
        button_download = tk.Button(self, text="Download Mod", width=17, command=self.download)
        button_download.grid(row=0, column=2, sticky="w", padx=20, pady=(10, 0))  # Top padding only

        # ✅ Back Button (Directly Below Download Button)
        button_back = tk.Button(self, text="Back", width=17, command=lambda: controller.show_frame("HomePage"))
        button_back.place(x = 292, y = 45)  # Small gap between buttons


    def download(self):
        """Called when the download button is clicked."""
        url = self.downloader.cur_select(None)  # Get selected mod URL
        if url:
            self.downloader.download_file(url)
        else:
            print("No mod selected for download.")

class ModDownloader:
    def __init__(self, listbox, mods):
        self.listbox = listbox
        self.mods = mods
        self.value = None  # Store the selected mod name

    def cur_select(self, evt):
        """Handles selection in the Listbox and stores the selected mod name and URL."""
        selected_index = self.listbox.curselection()
        if not selected_index:
            print("No mod selected.")
            self.value = None
            return None

        self.value = self.listbox.get(selected_index[0])  # Store selected mod name

        for mod in self.mods:
            if mod.get("name") == self.value:
                return mod.get("URL")  # Return URL of the selected mod

        print("Mod not found.")
        self.value = None
        return None

    def download_file(self, url):
        """Downloads the selected mod file."""
        if not url:
            print("Error: No URL provided.")
            return None

        if not self.value:
            print("Error: No selected mod name.")
            return None

        # ✅ Sanitize filename
        local_filename = "".join(c for c in self.value if c.isalnum() or c in (" ", "_", "-"))

        try:
            with requests.get(url, stream=True) as response:
                response.raise_for_status()  # ✅ Raise error for HTTP failures
                with open(local_filename, "wb") as file:
                    shutil.copyfileobj(response.raw, file)

            print(f"Download complete: {local_filename}")
            return local_filename

        except requests.exceptions.RequestException as e:
            print(f"Download failed: {e}")
            return None
