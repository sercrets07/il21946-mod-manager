import tkinter as tk
from screens.config import load_game_path
from screeninfo import get_monitors
from tkinter import StringVar
from tkinter import messagebox
import os

monitors = get_monitors()

class SetupScreen(tk.Frame):
    def __init__(self, parent, controller, game_path, game_conf_file):
        super().__init__(parent)
        self.controller = controller
        self.game_path = game_path  # ✅ Stores the main game directory
        self.game_conf_file = game_conf_file  # ✅ Stores the full conf.ini path

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)

        # ✅ Label to show the main game directory (not conf.ini)
        self.path_label = tk.Label(self, text=f"Game Path: {self.game_path or 'Not Set'}", font=("Arial", 12))
        self.path_label.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        label = tk.Label(self, text="Choose your IL-2 1946 game directory (Where it is installed)", font=("Arial", 14), fg="blue")
        label.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

        select_button = tk.Button(self, text="Select Directory",
                                  command=controller.select_game_folder)
        select_button.grid(row=3, column=0, sticky="ew", padx=20, pady=10)

        options = [f"{monitor.width}x{monitor.height}" for monitor in monitors]

        self.clicked = StringVar()
        self.clicked.set(options[0] if options else "No monitors detected")

        self.dropdown = tk.OptionMenu(self, self.clicked, *options)
        self.dropdown.grid(row=5, column=0, sticky="ew", padx=20, pady=10)

        btn_select_monitor = tk.Button(self, text="Select Monitor", command=self.select_monitor)
        btn_select_monitor.grid(row=6, column=0, padx=10, pady=5)

        back_button = tk.Button(self, text="Back",
                        command=self.go_back)
        back_button.grid(row=3, column=1, sticky="ew", padx=20, pady=10)

    def go_back(self):
        """Only go back if a valid game path is set. Otherwise, show an error."""
        if not self.game_path or not os.path.exists(self.game_path):  # ✅ Check if game path is missing or invalid
            messagebox.showerror("Error", "A Game Path is Required, Please Select One.")
        else:
             self.controller.show_frame("HomePage")  # ✅ Only go back if path exists



    def select_monitor(self):
        """Handle the monitor selection."""
        if not self.game_conf_file:
            print("❌ Error: Game path not set. Please select a game directory first.")
            return

        selected_monitor = self.clicked.get()
        print(f"✅ Selected Monitor: {selected_monitor}")

        width, height = selected_monitor.split('x')
        width, height = width.strip(), height.strip()

        with open(self.game_conf_file, 'r') as file:
            lines = file.readlines()

        line_to_replace_width = 5
        line_to_replace_height = 6

        if len(lines) > line_to_replace_height:
            lines[line_to_replace_height] = f"height={height}\n"
        if len(lines) > line_to_replace_width:
            lines[line_to_replace_width] = f"width={width}\n"

        with open(self.game_conf_file, 'w') as file:
            file.writelines(lines)

        print(f"✅ The resolution has been updated to {width}x{height} in conf.ini")

    def update_game_path(self):
        """Update the label with the saved game path."""
        self.path_label.config(text=f"Game Path: {self.game_path or 'Not Set'}")
