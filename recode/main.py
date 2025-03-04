import tkinter as tk
import os
import json
from tkinter import filedialog
from tkinter import messagebox
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# ✅ Import Screens
from screens.home import HomePage
from screens.setup import SetupScreen
from screens.config import save_game_path, load_game_path
from screens.manager import Mod_Manager
from screens.downloader import Down_Loader




CONFIG_FILE = os.path.join(os.path.expanduser("~"), "Documents", "recode", "config.json")
GAME_CONF_FILE = "conf.ini" # This is a place holder and is updated with actua; game path. 

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IL-2 1946 Mod Manager")
        self.geometry("600x400")
        self.maxsize(600, 400)
        self.minsize(600, 400)

        # ✅ Set background color for the main window
        self.configure(bg="#f3ddae")

        # ✅ Use grid() instead of pack()
        self.container = tk.Frame(self, bg="#f3ddae")
        self.container.grid(row=0, column=0, sticky="nsew")  # ✅ Use grid

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # ✅ Use grid for the frame too
        self.frame = tk.Frame(self, bg="#f3ddae", width=600, height=200)
        self.frame.grid(row=1, column=0, sticky="nsew")  # ✅ Fixed grid usage

        self.frames = {}

        # ✅ Get the game path (Only the directory)
        self.game_path = load_game_path()
        self.game_conf_file = None

        if self.game_path:
            self.game_conf_file = f"{self.game_path}/conf.ini"  # ✅ Only used for resolution updates

        # ✅ Loop through all frames and set their background
        for F in (HomePage, SetupScreen, Mod_Manager, Down_Loader):
            if F == SetupScreen:
                frame = F(parent=self.container, controller=self, game_path=self.game_path, game_conf_file=self.game_conf_file)
            else:
                frame = F(parent=self.container, controller=self)

            # ✅ Set background color for each frame
            frame.configure(bg="#f3ddae")
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.determine()

    # --------------------------
    # Determine Path
    # --------------------------
    def determine(self):
        """Only show error if user presses back, not on launch."""

        # ✅ If CONFIG_FILE doesn't exist, go to SetupScreen
        if not os.path.exists(CONFIG_FILE):
            self.show_frame("SetupScreen")  # ✅ Stay on SetupScreen
            return

        # ✅ Read the config file content
        with open(CONFIG_FILE, "r") as file:
            content = file.read().strip()  # ✅ Read file & remove extra spaces

        # ✅ If config file is empty, go to SetupScreen
        if not content:
            self.show_frame("SetupScreen")
            return

        # ✅ Load JSON safely
        data = json.loads(content) if content.startswith("{") else {}

        # ✅ Get saved game path
        game_path = data.get("game_path", "")

        # ✅ If the path is valid, go to HomePage
        if game_path and os.path.exists(game_path):
            self.show_frame("HomePage")
        else:
            self.show_frame("SetupScreen")  # ✅ Stay on SetupScreen if invalid path

    def select_game_folder(self):
        """Let the user select a game folder and save it."""
        folder = filedialog.askdirectory(title="Select IL-2 1946 Game Folder")
        
        if folder:  # ✅ Ensure folder is selected
            save_game_path(folder)  # ✅ Save the path
            global GAME_CONF_FILE
            GAME_CONF_FILE = os.path.join(folder, 'conf.ini')  # ✅ Update conf.ini path

            print(f"Selected game folder: {folder}")  # ✅ Debug message
            print(f"Saved path in JSON: {load_game_path()}")  # ✅ Verify save operation

            self.show_frame("HomePage")  # ✅ Switch to HomePage after saving

    def show_frame(self, page_name):
        """Switch to the given frame and update path if needed."""
        frame = self.frames[page_name]
        frame.tkraise()

        # ✅ Only call update_game_path() when showing SetupScreen
        if page_name == "SetupScreen":
            frame.update_game_path()

# --------------------------
# Run the Application
# --------------------------
if __name__ == "__main__":
    app = Application()
    app.mainloop()
