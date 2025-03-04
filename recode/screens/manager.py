from curses.textpad import Textbox
import tkinter as tk
from tkinter import Toplevel
import json
import os
from PIL import Image, ImageTk
import uuid
import requests
import base64


deviceuuid = uuid.uuid4()
uuid_file = "device_uuid.txt"



#---------------------------
# Save UUID to JSON
#---------------------------

def get_or_create_uuid():
     if os.path.exists(uuid_file):
          with open(uuid_file, "r") as file:
               return file.read().strip()
     else:
          new_uuid = str(deviceuuid)
          with open(uuid_file, "w") as file:
               file.write(new_uuid)
          return new_uuid
     

perma_device_uuid = get_or_create_uuid()

#---------------------------
# Check for /download
#---------------------------
def ensure_suffix(text, suffix):
     if not text.endswith(suffix):
          text+= suffix
     return text


import requests

#---------------------------
# Server Implementation
#---------------------------
import requests
import base64
import json

SERVER_URL = "http://127.0.0.1:5100"

def upload_file(file_path):
    url = f"{SERVER_URL}/upload_file"
    with open(file_path, "rb") as file:  # ✅ Fix: Using `with open()`
        files = {"file": file}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        print(f"✅ Upload Successful")
    else:
        print(f"❌ Upload Failed: {response.json()}")

def download_file(filename, save_path):
    url = f"{SERVER_URL}/download/{filename}"
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):  # ✅ Fix: Buffered write
                file.write(chunk)
        print(f"✅ Download Successful: {save_path}")
    else:
        print(f"❌ Download Failed: {response.json()}")



#---------------------------
# Define Get Text Method
#---------------------------
def get_text(text_box, text_box2, selection):
    user_input = text_box.get("1.0", tk.END).strip()
    link = text_box2.get("1.0", tk.END).strip()
    link = ensure_suffix(link, "/download")

    if selection == "Object":
        mod_type = "Object"
    elif selection == "Aircraft":
        mod_type = "Aircraft"
    elif selection == "Map":
        mod_type = "Map"
    else: 
        mod_type = "Unknown"

    #---------------------------
    # JSON function to read and write mods
    # --------------------------
    mod_pack = {
        "name" : user_input,
        "URL" : link,
        "type" : mod_type,
        "ID" : perma_device_uuid
    }

    write(mod_pack)

#-----------------------------
# Prepare PopUp window for use
#-----------------------------
def show_popup():
     popup = Toplevel()
     popup.title("Error")
     popup.geometry("300x200")
     
     # ✅ Load and resize image using Pillow
     original_image = Image.open("X.png")  # Load image
     resized_image = original_image.resize((75, 75))  # Resize (Width, Height)
     popup_image = ImageTk.PhotoImage(resized_image)  # Convert to Tkinter format

     # ✅ Store image in an instance variable to prevent garbage collection
     popup.label_image = popup_image  

     # ✅ Display the resized image
     label = tk.Label(popup, image=popup_image)
     label.pack(pady=10)
     label = tk.Label(popup, text="Name already exists, Please enter a different Name.", font=("Arial", 12))
     label.pack(pady=20)

     close_button = tk.Button(popup, text="Close", command=popup.destroy)
     close_button.pack(pady=10)

#-----------------------------
# Prepare PopUp Window for Use
#-----------------------------
def show_gpopup():
     popup = Toplevel()
     popup.title("Success!")
     popup.geometry("300x200")
     
     # ✅ Load and resize image using Pillow
     original_image = Image.open("check.png")  # Load image
     resized_image = original_image.resize((75, 75))  # Resize (Width, Height)
     popup_image = ImageTk.PhotoImage(resized_image)  # Convert to Tkinter format

     # ✅ Store image in an instance variable to prevent garbage collection
     popup.label_image = popup_image  

     # ✅ Display the resized image
     label = tk.Label(popup, image=popup_image)
     label.pack(pady=10)
     label = tk.Label(popup, text="Mod Added Succesfull!", font=("Arial", 12))
     label.pack(pady=20)

     close_button = tk.Button(popup, text="Ok", command=popup.destroy)
     close_button.pack(pady=10)



def write(mod_pack):
    download_file("mod_pack.json", "mod_pack.json")  # ✅ Fix: Proper function call

    file_name = "mod_pack.json"

    # ✅ Read existing data
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        with open(file_name, "r") as file:
            data = json.load(file)
    else:
        data = []

    # ✅ Check for duplicate names and URLs
    existing_names = {entry["name"] for entry in data}
    double_link = {entry["URL"] for entry in data}

    if mod_pack["name"] in existing_names or mod_pack["URL"] in double_link:
        show_popup()
        return False  # ❌ Error: Mod already exists

    # ✅ Add new mod entry
    data.append(mod_pack)

    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

    upload_file(file_name)  # ✅ Fix: Upload after writing
    show_gpopup()
    return True

def read():
    """Reads `mod_pack.json` and returns its content."""
    with open("mod_pack.json", "r") as file:
        return json.load(file)

# --------------------------
# Define Mod Manager
# --------------------------
import tkinter as tk

class Mod_Manager(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configure grid layout (3 columns for proper centering)
        self.columnconfigure(0, weight=1)  # Left space
        self.columnconfigure(1, weight=2)  # Main content
        self.columnconfigure(2, weight=1)  # Right space

        # Row configuration to avoid stretching
        for i in range(7):
            self.rowconfigure(i, weight=0)

        # Dropdown menu variable
        self.selected_option = tk.StringVar(self)
        self.selected_option.set("Object")

        # Name Label & Textbox
        self.label = tk.Label(self, text="Name:", font=("Arial", 14))
        self.label.grid(row=0, column=1, sticky="ew", padx=20, pady=2)

        self.text_box = tk.Text(self, width=50, height=1)
        self.text_box.grid(row=1, column=1, sticky="ew", padx=20, pady=1)

        # URL Label & Textbox
        self.label2 = tk.Label(self, text="URL", font=("Arial", 14))
        self.label2.grid(row=2, column=1, sticky="ew", padx=20, pady=2)

        self.text_box2 = tk.Text(self, width=50, height=1)
        self.text_box2.grid(row=3, column=1, sticky="ew", padx=20, pady=1)

        # Type Label & Dropdown
        self.label3 = tk.Label(self, text="Select a Type:", font=("Arial", 14))
        self.label3.grid(row=4, column=1, sticky="ew", padx=20, pady=2)

        OpMen = tk.OptionMenu(self, self.selected_option, "Object", "Aircraft", "Map")
        OpMen.grid(row=5, column=1, sticky="ew", padx=20, pady=2)

        # Frame to center buttons
        button_frame = tk.Frame(self)
        button_frame.grid(row=6, column=1, columnspan=1, pady=10)

        add_button = tk.Button(button_frame, text="Add Mod", width=17, command=self.send_selection)
        add_button.pack(side="left", padx=10)

        back_button = tk.Button(button_frame, text="Back", width=17, command=lambda: controller.show_frame("HomePage"))
        back_button.pack(side="left", padx=10)

    def send_selection(self):
        """Clears text boxes and calls get_text()"""
        selection = self.selected_option.get()
        get_text(self.text_box, self.text_box2, selection)

        # Clear the text boxes
        self.text_box.delete("1.0", tk.END)
        self.text_box2.delete("1.0", tk.END)

    def get_selection(self):
        """Returns dropdown selection."""
        return self.selected_option.get()
    
    def send_selection(self):
        """Gets user input and clears text boxes after sending data."""
        selection = self.get_selection()
        get_text(self.text_box, self.text_box2, selection)
        
        # Clear the text boxes
        self.text_box.delete("1.0", tk.END)
        self.text_box2.delete("1.0", tk.END)
