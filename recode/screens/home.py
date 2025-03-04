import tkinter as tk

# --------------------------
# Define Home Page
# --------------------------
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ✅ Configure this frame to expand within container
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)  # Space above button
        self.rowconfigure(1, weight=0)  # Button stays in this row
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)    # Space below button

        # Button to go to the Settings page
        button = tk.Button(self, text="Settings",
                           bg="#f3ddae", fg="black", font=("Arial", 12),
                           command=lambda: controller.show_frame("SetupScreen"))
        
        # ✅ Place button in row 1, centered at the top
        button.grid(row=1, column=0, sticky="ew", padx=20, pady=5) 

        # Button to go to the Mod Manager page
        button = tk.Button(self, text="Mod Manager",
                           command=lambda: controller.show_frame("Mod_Manager"))
        
        button.grid(row=2, column = 0, sticky="ew", padx=20, pady=2)

                # Button to go to the Mod Manager page
        button = tk.Button(self, text="Download Mods",
                           command=lambda: controller.show_frame("Down_Loader"))
        
        button.grid(row=3, column = 0, sticky="ew", padx=20, pady=2)
