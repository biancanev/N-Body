"""
Simple installer using tkinter.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from urllib.request import urlretrieve

root = tk.Tk()
root.withdraw()

installation_path = filedialog.askdirectory(title="Select Installation Path")

if installation_path:
    urlretrieve("https://raw.githubusercontent.com/biancanev/N-Body/refs/heads/main/dist/simulator.exe", installation_path + "/simulator.exe")
    urlretrieve("https://raw.githubusercontent.com/biancanev/N-Body/refs/heads/main/dist/simulation_config.json", installation_path + "/simulation_config.json")
    messagebox.showinfo("Installation Successful", f"Successfully installed simulator to {installation_path}.")
    
else:
    messagebox.showinfo("Installation Aborted", "No installation path was specified. Aborted installation.")