"""
Simple installer using tkinter.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from urllib.request import urlretrieve
import zipfile

root = tk.Tk()
root.withdraw()

installation_path = filedialog.askdirectory(title="Select Installation Path")

if installation_path:
    urlretrieve("https://github.com/biancanev/N-Body/raw/refs/heads/master/dist/rev2/release_rev2.zip", installation_path + "/simulator_rev2.zip")
    with zipfile.ZipFile(installation_path + "/simulator_rev2.zip", 'r') as zip_ref:
        zip_ref.extractall(installation_path)
    messagebox.showinfo("Installation Successful", f"Successfully installed simulator to {installation_path}.")
    
else:
    messagebox.showinfo("Installation Aborted", "No installation path was specified. Aborted installation.")