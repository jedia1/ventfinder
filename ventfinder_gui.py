#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 15:36:24 2025

@author: jennadia
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import ventfinder

def execute_ventfinder():
    try:
        mirova_csv = csv_file_var.get()
        dem = dem_file_var.get()
        path_to_results = path_to_results_var.get()
        threshold = float(threshold_var.get())
        project_name = project_name_var.get()
        shapefiles = shapefiles_var.get()
        if mirova_csv == '':
            messagebox.showerror('Error', 'Please choose a MIROVA .csv file.')
            return
    
        if dem == '':
            messagebox.showerror('Error', 'Please choose a DEM file.')
            return
        
        if path_to_results == '':
            messagebox.showerror('Error', 'Please choose a path to results.')
            return
            
        if project_name == '':
            messagebox.showerror('Error', 'Please enter a project name.')
            return
        
        if threshold > 1 or threshold < 0:
            messagebox.showerror('Error','Threshold value must be between 0 and 1.')
            
        if shapefiles:
            epsg_code = epsg_code_var.get()
            if epsg_code == '':
                messagebox.showerror('Error', "You have selected 'Yes' to 'Create shapefiles for MIROVA data and results.' An EPSG code in required.")
                return
            
        else:
            epsg_code = ''
        
        ventfinder.run_ventfinder(mirova_csv, dem, path_to_results, project_name, epsg_code=epsg_code, threshold=threshold, mask=None, shapefiles=shapefiles)
    
        messagebox.showinfo('Success', 'Ventfinder executed successfully.')
    
    except FileNotFoundError as f_error:
        messagebox.showerror('Error', f_error)
    
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
    
def enable_epsg():
    if shapefiles_var.get():
        entryEPSG.configure(state='normal')
    else:
        epsg_code_var.set('')
        entryEPSG.configure(state='disabled')
        
def close():
    window.destroy()


window = tk.Tk()
window.geometry('900x500')
window.title("Ventfinder")

csv_file_var = tk.StringVar()
dem_file_var = tk.StringVar()
path_to_results_var = tk.StringVar()
threshold_var = tk.StringVar(value='0.5')
project_name_var = tk.StringVar()
shapefiles_var =tk.BooleanVar()
epsg_code_var = tk.StringVar()

# choose .csv file
lblCSV = tk.Label(window, text="Choose .csv file: ", font=('Arial', 12))
lblCSV.grid(row=0, column=0, sticky='w')
entryCsv = tk.Entry(window, textvariable=csv_file_var, width=40)
entryCsv.grid(row=0, column=1)
btnBrowseCsv = tk.Button(window, text="Browse", command=choose_csv_file_path)
btnBrowseCsv.grid(row=0, column=2, sticky='w')

# choose DEM
lblDEM = tk.Label(window, text="Choose DEM file: ", font=('Arial', 12))
lblDEM.grid(row=1, column=0, sticky='w')
entryDEM = tk.Entry(window, textvariable=dem_file_var, width=40)
entryDEM.grid(row=1, column=1)
btnBrowseDEM = tk.Button(window, text="Browse", command=choose_dem_file_path)
btnBrowseDEM.grid(row=1, column=2, sticky='w')

# choose path to results
lblPath = tk.Label(window, text="Choose path to results: ", font=('Arial', 12))
lblPath.grid(row=2, column=0, sticky='w')
entryPath = tk.Entry(window, textvariable=path_to_results_var, width=40)
entryPath.grid(row=2, column=1)
btnBrowsePath = tk.Button(window, text="Browse", command=choose_path_to_results)
btnBrowsePath.grid(row=2, column=2, sticky='w')

# project name
lblName = tk.Label(window, text="Enter Project Name: ", font=('Arial', 12)) 
lblName.grid(row=3, column=0, sticky='w')
entryName = tk.Entry(window, textvariable=project_name_var, width=40)
entryName.grid(row=3, column=1)

# threshold
lblThreshold = tk.Label(window, text="rCTR Threshold: ", font=('Arial', 12))
lblThreshold.grid(row=4, column=0, sticky='w')
entryThreshold = tk.Entry(window, textvariable=threshold_var, state=tk.DISABLED, width=40)
entryThreshold.grid(row=4, column=1)
btnThreshold = tk.Button(window, text='Enter custom threshold', command=enable_threshold)
btnThreshold.grid(row=4, column=2, sticky='w')

# epsg code
lblEPSG = tk.Label(window, text='Enter EPSG Code (numbers only): ', font=('Arial', 12))
lblEPSG.grid(row=6, column=0, sticky='w')
entryEPSG = tk.Entry(window, textvariable=epsg_code_var, state=tk.DISABLED, width=40)
entryEPSG.grid(row=6, column=1)

# create shapefiles
lblShapefiles = tk.Label(window, text= 'Create shapefiles for MIROVA data and results? ', font=('Arial', 12))
lblShapefiles.grid(row=5, column=0, sticky='w')
chkbxShapefiles =tk.Checkbutton(window, text='Yes', variable=shapefiles_var, command=enable_epsg)
chkbxShapefiles.grid(row=5, column=1)

btnVentfinder = tk.Button(window,text='Run Ventfinder', command=execute_ventfinder)
btnVentfinder.grid(row=7, column=1)

btnClose = tk.Button(window, text='Exit', command=close)
btnClose.grid(row=8, column=1)

window.mainloop()