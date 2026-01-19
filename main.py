import os
import sys
import json
from customtkinter import *
from tkinter import PhotoImage
from PIL import Image
import screen_brightness_control as sbc
import webbrowser
import winreg
from tkinter import messagebox  # For error messages

# -------------------------------
CONFIG_FILE = "config.json"
set_default_color_theme("blue")

# -------------------------------
# Config Load/Save
# -------------------------------
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            with open(CONFIG_FILE, 'x') as f:
                f.write("{}")
            return {"theme": get_appearance_mode().lower(), "auto_start": False}
        except Exception as e:
            messagebox.showerror("Config Error", f"Failed to load config.json", detail=str(e), icon='error')
            return {"theme": get_appearance_mode().lower(), "auto_start": False}
    return {"theme": get_appearance_mode().lower(), "auto_start": False}

def save_config():
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
    except Exception as e:
        messagebox.showerror("Config Error", f"Failed to save config.json", detail=str(e), icon='error')

# -------------------------------
# Brightness Functions
# -------------------------------
def get_brightness():
    try:
        return sbc.get_brightness(display=0)[0]
    except Exception as e:
        messagebox.showerror("Brightness Error", f"Failed to get brightness", detail=str(e), icon='error')
        return 50

def set_brightness(value):
    try:
        sbc.set_brightness(int(value), display=0)
        LABEL3.configure(text=f"Level ({int(value)}%)")
    except Exception as e:
        messagebox.showerror("Brightness Error", f"Failed to set brightness", detail=str(e), icon='error')

# -------------------------------
# Windows Auto Start
# -------------------------------
def set_auto_start(enable: bool):
    """Enable or disable auto-start on Windows."""
    try:
        script_path = os.path.abspath(sys.argv[0])
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        if enable:
            winreg.SetValueEx(key, "BrightnessController", 0, winreg.REG_SZ, f'"{sys.executable}" "{script_path}"')
        else:
            try:
                winreg.DeleteValue(key, "BrightnessController")
            except FileNotFoundError:
                pass
        winreg.CloseKey(key)
    except Exception as e:
        messagebox.showerror("Auto-start Error", f"Failed to set auto-start", detail=str(e), icon='error')

# -------------------------------
# Theme Functions
# -------------------------------
def apply_theme(theme_name):
    try:
        set_appearance_mode(theme_name.lower())
        config["theme"] = theme_name.lower()
        save_config()
    except Exception as e:
        messagebox.showerror("Theme Error", f"Failed to apply theme", detail=str(e), icon='error')

# -------------------------------
# About Dialog
# -------------------------------
def about():
    try:
        dialog = CTkToplevel(root)
        dialog.title("About")
        dialog.transient(root)
        dialog.grab_set()
        dialog.overrideredirect(True)

        # ---- Main container ----
        main_frame = CTkFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # ---- Left: Icon inside dialog ----
        icon_frame = CTkFrame(main_frame, fg_color="transparent")
        icon_frame.pack(side="right", padx=(0, 15))
        try:
            pil_image = Image.open("icon.png")
            ctk_icon = CTkImage(light_image=pil_image, dark_image=pil_image, size=(100, 100))
            CTkLabel(icon_frame, image=ctk_icon, text="").pack()
        except Exception:
            CTkLabel(icon_frame, text="💡", text_color='yellow', font=CTkFont(size=100)).pack()

        # ---- Right: Text ----
        text_frame = CTkFrame(main_frame, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True)

        CTkLabel(text_frame, text="Brightness Controller", font=CTkFont(size=22, weight="bold")).pack(anchor="w")
        CTkLabel(text_frame, text="Version 1.0.0", font=CTkFont(size=13), text_color=("gray30", "gray70")).pack(anchor="w", pady=(0,6))
        CTkLabel(text_frame, text=(
            "A lightweight desktop utility to control\n"
            "screen brightness easily and efficiently.\n\n"
            "Built with Python, CustomTkinter,\n"
            "and screen_brightness_control."
        ), justify="left", wraplength=250).pack(anchor="w")
        CTkLabel(text_frame, text="\nAuthor: Muhammad Abubakar Siddique Ansari", font=CTkFont(size=12, weight="bold")).pack(anchor="w")

        # ---- Buttons ----
        button_frame = CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 10))

        CTkButton(button_frame, text="Close", width=90, command=dialog.destroy, fg_color='red', hover_color="#f56969").pack(side="right", padx=15)
        CTkButton(button_frame, text="GitHub", width=90, command=lambda: webbrowser.open("https://github.com/Ansari-Codes")).pack(side="left", padx=(15, 2))
        CTkButton(button_frame, text="Portfolio", width=90, command=lambda: webbrowser.open("https://ansari-codes.github.io/portfolio/"), fg_color='green').pack(side="left", padx=1)

        dialog.resizable(False, False)
        width, height = 450, 250

        # Get root window position
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        root_width = root.winfo_width()
        root_height = root.winfo_height()

        # Center dialog relative to root
        x = root_x + (root_width // 2) - (width // 2)
        y = root_y + (root_height // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

    except Exception as e:
        messagebox.showerror("About Error", "Failed to open About dialog", detail=str(e), icon='error')


# -------------------------------
# Center the window
# -------------------------------
def center_window(window, width=500, height=200):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# -------------------------------
# UI Setup
# -------------------------------
root = CTk()
root.title("Brightness Controller")

# ICON SETUP
try:
    root.iconbitmap("icon.ico")
    icon_png = PhotoImage(file="icon.png")
    root.iconphoto(False, icon_png)
except Exception as e:
    messagebox.showwarning("Icon Warning", "Failed to load app icon", detail=str(e))

root.configure(fg_color=['gray92', 'gray14'])
center_window(root, 500, 200)
root.resizable(False, False)

LABEL0 = CTkLabel(root, text="Brightness Controller", fg_color="transparent",
                  text_color=("#000000", "#DCE4EE"), pady=19,
                  font=CTkFont(family="Arial Greek", size=30, weight="bold", slant="roman"))
LABEL0.pack(fill="x")

FRAME2 = CTkFrame(root, height=50)
FRAME2.pack_propagate(False)
FRAME2.pack(padx=30, fill="x")

LABEL3 = CTkLabel(FRAME2, text=f"Level ({get_brightness()}%)", fg_color="transparent",
                  text_color=("#000000", "#DCE4EE"), font=CTkFont(size=20, weight="bold"))
LABEL3.pack(padx=(14,0), side="left")

SLIDER4 = CTkSlider(FRAME2, from_=0, to=100, number_of_steps=100,
                    command=set_brightness,
                    orientation="horizontal",
                    border_color=("#bdb9b9", "#3d3d3d"),
                    progress_color=("#f9cf40", "#b78f06"),
                    button_color=("#0080ff", "#0080ff"),
                    button_hover_color=("#ffffff", "#eeeeee"),
                    hover=True,
                    state="normal",
                    fg_color=("#939BA2", "#ffe7c8"))
SLIDER4.pack(padx=15, expand=1, fill="x", side="right")
SLIDER4.set(get_brightness())

# -------------------------------
# Load config & apply theme
# -------------------------------
config = load_config()
apply_theme(config.get("theme", "system").lower())

SEGMENTEDBUTTON5 = CTkSegmentedButton(root, values=["Dark", "Light"],
                                    fg_color=("#c0c0c0", "gray29"),
                                    bg_color="transparent",
                                    dynamic_resizing=True,
                                    font=CTkFont(size=15),
                                    command=apply_theme)
SEGMENTEDBUTTON5.pack(padx=(32,0), side="left")
SEGMENTEDBUTTON5.set(config.get("theme", "system").capitalize())

BUTTON6 = CTkButton(root, text="ℹ About", width=70, font=CTkFont(size=15), command=about)
BUTTON6.pack(padx=(0,32), side="right")

def toggle_autostart():
    enabled = bool(CHECKBOX7.get())
    set_auto_start(enabled)
    config["auto_start"] = enabled
    save_config()

CHECKBOX7 = CTkCheckBox(root, text="Activate on Windows Startup",
                        checkbox_width=18, checkbox_height=18,
                        corner_radius=6, border_width=2,
                        font=CTkFont(size=15),
                        command=toggle_autostart)
CHECKBOX7.pack(padx=10, side="left")

if config.get("auto_start", False):
    CHECKBOX7.select()
    toggle_autostart()

# -------------------------------
root.mainloop()
