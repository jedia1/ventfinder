#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 15:36:24 2025

@author: jennadia
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def choose_csv_file_path():
    csv_file_path = filedialog.askopenfilename()
    csv_file_var.set(csv_file_path)
    
def choose_dem_file_path():
    dem_file_path = tk.filedialog.askopenfilename()
    dem_file_var.set(dem_file_path)

def choose_path_to_results():
    path = tk.filedialog.askdirectory()
    path_to_results_var.set(path)
    
def enable_threshold():
    entryThreshold.configure(state='normal')

window = tk.Tk()
window.geometry('700x500')
window.title("Ventfinder")

csv_file_var = tk.StringVar()
dem_file_var = tk.StringVar()
path_to_results_var = tk.StringVar()
threshold_var = tk.StringVar(value='0.5')
project_name_var = tk.StringVar()

# choose .csv file
lblCSV = tk.Label(window, text="Choose .csv file: ", font=('Arial', 12))
lblCSV.grid(row=0, column=0, sticky='w')
entryCsv = tk.Entry(window, textvariable=csv_file_var, width=40)
entryCsv.grid(row=0, column=1)
btnBrowseCsv = tk.Button(window, text="Browse", command=choose_csv_file_path)
btnBrowseCsv.grid(row=0, column=2, sticky='w')

# choose DEM
lblDEM = tk.Label(window, text="Choose DEM file: ", font=('Arial', 12))
lblDEM.grid(row=2, column=0, sticky='w')
entryDEM = tk.Entry(window, textvariable=dem_file_var, width=40)
entryDEM.grid(row=2, column=1)
btnBrowseDEM = tk.Button(window, text="Browse", command=choose_dem_file_path)
btnBrowseDEM.grid(row=2, column=2, sticky='w')

# choose path to results
lblPath = tk.Label(window, text="Choose path to results: ", font=('Arial', 12))
lblPath.grid(row=4, column=0, sticky='w')
entryPath = tk.Entry(window, textvariable=path_to_results_var, width=40)
entryPath.grid(row=4, column=1)
btnBrowsePath = tk.Button(window, text="Browse", command=choose_path_to_results)
btnBrowsePath.grid(row=4, column=2, sticky='w')

# project name
lblName = tk.Label(window, text="Enter Project Name: ", font=('Arial', 12)) 
lblName.grid(row=6, column=0, sticky='w')
entryName = tk.Entry(window, textvariable=project_name_var, width=40)
entryName.grid(row=6, column=1)

# threshold
lblThreshold = tk.Label(window, text="rCTR Threshold: ", font=('Arial', 12))
lblThreshold.grid(row=8, column=0, sticky='w')
entryThreshold = tk.Entry(window, textvariable=threshold_var, state=tk.DISABLED, width=40)
entryThreshold.grid(row=8, column=1)
btnThreshold = tk.Button(window, text='Enter custom threshold', command=enable_threshold)
btnThreshold.grid(row=8, column=2, sticky='w')


window.mainloop()