#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 17:50:01 2025

@author: jennadia
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
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
        
        if not os.path.isfile(mirova_csv):
            messagebox.showerror('Error', f'{mirova_csv} file does not exist.')
            return
    
        if dem == '':
            messagebox.showerror('Error', 'Please choose a DEM file.')
            return
        
        if not os.path.isfile(dem):
            messagebox.showerror('Error', f'{dem} file does not exist.')
            return
        
        if path_to_results == '':
            messagebox.showerror('Error', 'Please choose a path to results.')
            return
        
        if not os.path.exists(path_to_results):
            messagebox.showerror('Error', f'{path_to_results} is not a directory')
            return
            
        if project_name == '':
            messagebox.showerror('Error', 'Please enter a project name.')
            return
        
        if threshold > 1 or threshold < 0:
            messagebox.showerror('Error','Threshold value must be between 0 and 1.')
            return
            
        if shapefiles:
            epsg_code = epsg_code_var.get()
            if epsg_code == '':
                messagebox.showerror('Error', "You have selected 'Yes' to 'Create shapefiles for MIROVA data and results.' An EPSG code in required.")
                return
            
        else:
            epsg_code = ''
        
        ventfinder.run_ventfinder(mirova_csv, dem, path_to_results, project_name, epsg_code=epsg_code, threshold=threshold, mask=None, shapefiles=shapefiles)
    
        messagebox.showinfo('Success', 'Ventfinder executed successfully.')
    
    except Exception as error:
        messagebox.showerror('Error', error)
        return
    
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
        
def change_page(frame):
    frame.tkraise()
        
def close():
    window.destroy()

window = tk.Tk()
window.geometry('900x300')
window.title("Ventfinder")

pageHelp = tk.Frame(window)
pageHelp.grid(row=0, column=0, sticky='nsew')

pageAbout = tk.Frame(window)
pageAbout.grid(row=0, column=0, sticky='nsew')

page1 = tk.Frame(window)
page1.grid(row=0, column=0, sticky='nsew')

csv_file_var = tk.StringVar()
dem_file_var = tk.StringVar()
path_to_results_var = tk.StringVar()
threshold_var = tk.StringVar(value='0.5')
project_name_var = tk.StringVar()
shapefiles_var =tk.BooleanVar()
epsg_code_var = tk.StringVar()


# choose .csv file
lblCSV = tk.Label(page1, text="Choose .csv file: ", font=('Arial', 12))
lblCSV.grid(row=0, column=0, sticky='w')
entryCsv = tk.Entry(page1, textvariable=csv_file_var, width=40)
entryCsv.grid(row=0, column=1)
btnBrowseCsv = tk.Button(page1, text="Browse", command=choose_csv_file_path)
btnBrowseCsv.grid(row=0, column=2, sticky='w')

# choose DEM
lblDEM = tk.Label(page1, text="Choose DEM file: ", font=('Arial', 12))
lblDEM.grid(row=1, column=0, sticky='w')
entryDEM = tk.Entry(page1, textvariable=dem_file_var, width=40)
entryDEM.grid(row=1, column=1)
btnBrowseDEM = tk.Button(page1, text="Browse", command=choose_dem_file_path)
btnBrowseDEM.grid(row=1, column=2, sticky='w')

# choose path to results
lblPath = tk.Label(page1, text="Choose path to results: ", font=('Arial', 12))
lblPath.grid(row=2, column=0, sticky='w')
entryPath = tk.Entry(page1, textvariable=path_to_results_var, width=40)
entryPath.grid(row=2, column=1)
btnBrowsePath = tk.Button(page1, text="Browse", command=choose_path_to_results)
btnBrowsePath.grid(row=2, column=2, sticky='w')

# project name
lblName = tk.Label(page1, text="Enter Project Name: ", font=('Arial', 12)) 
lblName.grid(row=3, column=0, sticky='w')
entryName = tk.Entry(page1, textvariable=project_name_var, width=40)
entryName.grid(row=3, column=1)

# threshold
lblThreshold = tk.Label(page1, text="rCTR Threshold: ", font=('Arial', 12))
lblThreshold.grid(row=4, column=0, sticky='w')
entryThreshold = tk.Entry(page1, textvariable=threshold_var, state=tk.DISABLED, width=40)
entryThreshold.grid(row=4, column=1)
btnThreshold = tk.Button(page1, text='Enter custom threshold', command=enable_threshold)
btnThreshold.grid(row=4, column=2, sticky='w')

# epsg code
lblEPSG = tk.Label(page1, text='Enter EPSG Code (numbers only): ', font=('Arial', 12))
lblEPSG.grid(row=6, column=0, sticky='w')
entryEPSG = tk.Entry(page1, textvariable=epsg_code_var, state=tk.DISABLED, width=40)
entryEPSG.grid(row=6, column=1)

# create shapefiles
lblShapefiles = tk.Label(page1, text= 'Create shapefiles for MIROVA data and' +
                         ' results?', font=('Arial', 12))
lblShapefiles.grid(row=5, column=0, sticky='w')
chkbxShapefiles =tk.Checkbutton(page1, text='Yes', variable=shapefiles_var, command=enable_epsg)
chkbxShapefiles.grid(row=5, column=1, sticky='w')

btnVentfinder = tk.Button(page1,text='Run Ventfinder', command=execute_ventfinder)
btnVentfinder.grid(row=7, column=1)

btnClose = tk.Button(page1, text='Exit', command=close)
btnClose.grid(row=8, column=1)

btnAbout = tk.Button(page1, text='About', command=lambda:change_page(pageAbout))
btnAbout.grid(row=8, column=0, sticky='w')

btnHelp = tk.Button(page1, text='Help', command=lambda:change_page(pageHelp))
btnHelp.grid(row=7, column=0, sticky='w')

lblHelp = tk.Label(pageHelp, text='Instructions', font=('Arial', 18))
lblHelp.grid(row=0, column=0, sticky='w')

txtHelp = tk.Text(pageHelp, wrap=tk.WORD, width=90, height=12, font=('Arial', 12))
txtHelp.grid(row=1, column=0)

csv_help_txt = 'Choose csv file: This is a .csv file provided by the MIROVA system containing the radiances, locations, and acquisition data of alerted MIROVA pixels. You may select a file by clicking "browse" or type a full path. \n \n'
dem_help_txt = 'Chosse DEM: This is a geotiff or ASCII file. Must be a regular grid in UTM coordinates.You may select a file by clicking "browse" or type a full path. If the MIROVA .csv file contains pixels outside the extent of the DEM, these pixels will be excluded from analysis and performance will be degraded. \n \n'
path_to_results_help_txt = 'Choose path to results: This is the folder to which all of your results will be written. You may select a file by clicking "browse" or type a full path. \n \n'
project_name_help_txt = 'Enter project name: This name will be appended to all output files. \n \n'
threshold_help_txt = 'rCTR Threshold: The default rCTR threshold value is 0.5. To change this value, click "Enter custom threshold" and enter a new threshold in the entry box. For more information on rCTR, see "About" tab. \n \n'
create_shapefiles_help_txt = 'Create shapefiles for MIROVA data and results: Selecting this options means that ESRI shapefiles will be generated for (1) the MIROVA data in the MIROVA .csv file, (2) the MIROVA pixels remaining after thermal thresholding, and (3) the final selection of MIROVA pixels. If you select "yes", you must provide an EPSG code for the UTM zone that contains your volcano of interest. Please type numbers only for the EPSG code. For example, if your volcano is in EPSG 32715/UTM Zone 15S, please only enter 32715. \n \n'

txtHelp.insert(tk.END, csv_help_txt)
txtHelp.insert(tk.END, dem_help_txt)
txtHelp.insert(tk.END, path_to_results_help_txt)
txtHelp.insert(tk.END, project_name_help_txt)
txtHelp.insert(tk.END, threshold_help_txt)
txtHelp.insert(tk.END, create_shapefiles_help_txt)

ysHelp = tk.Scrollbar(pageHelp, orient='vertical', command=txtHelp.yview)
txtHelp['state'] = 'disabled'
txtHelp['yscrollcommand'] = ysHelp.set
ysHelp.grid(row=1, column=1)

btnBackHelp = tk.Button(pageHelp, text='Back', command=lambda:change_page(page1))
btnBackHelp.grid(row=2, column=0)

text = '''
The purpose of this code is to localize effusive volcanic vents at the start of an eruption using data collected by the Visible Infrared Imaging Radiometer Suite (VIIRS) and processed by the Middle Infrared Observations of Volanic Activity (MIROVA) algorithm (Coppola et al., 2016, Coppola et al., 2020, Campus et al., 2022). It is optimized for the VIIRS 375 m resolution imaging bands in the thermal and infrared ranges. VIIRS 375 data is obtained from the MIROVA team in a .csv file, which the Ventfinder reads. A DEM for the volcano of interest is also required for the Ventfinder.

The Ventfinder works by adding the middle infrared (MIR) and thermal infrared (TIR) radiances together for each MIROVA-alerted pixel. The resulting value is the combined thermal radiance (CTR). The CTR values are normalized to the largest CTR value; the normalized value is called the relative CTR or rCTR value. The ventfinder then delineates clusters of pixels with an rCTR value greater than or equal to a threshold. The default thershold is 0.5, but this may be changed by the user. Then, it re-normalizes rCTR to the highest rCTR value in each cluster; this value is called rCTR'. Pixels with rCTR' less than the threshold are dropped from their clusters and no longer considered. Next, the average elevation is calculated for each remaining pixel (it is an average elevation because the DEM resolution is likely much finer that the MIROVA pixel resoluion). For each cluster, the pixel with the highest average elevation is selected, and the selected pixels' center UTM coordiantes and average elevation are written to a .csv file. These selected pixels are presumed likliest to contain an effusive vent.

This is distributed with no guarantee that it can accurately predict teh eruptive vent location.

This code was written with python 3.11 and uses the packages NumPy, pandas, rasterio, fiona. The GUI was built using tkinter.

References:

Campus, A., Laiolo, M., Massimetti, F., & Coppola, D. (2022). The transition from MODIS to VIIRS for global volcano thermal monitoring. Sensors, 22(5), 1713.

Coppola, D., Laiolo, M., Cigolini, C., Delle Donne, D., & Ripepe, M. (2016). Enhanced volcanic hot-spot detection using MODIS IR data: results from the MIROVA system.

Coppola, D., Laiolo, M., Cigolini, C., Massimetti, F., Delle Donne, D., Ripepe, M., ... & William, R. (2020). Thermal remote sensing for global volcano monitoring: experiences from the MIROVA system. Frontiers in Earth Science, 7, 362.
'''

lblAbout = tk.Label(pageAbout, text='About', font=('Arial', 18))
lblAbout.grid(row=0, column=0, sticky='w')
txtAbout = tk.Text(pageAbout, wrap=tk.WORD, width=90, height=12,font=('Arial', 12))
txtAbout.grid(row=1, column=0, sticky='nsew')
ysAbout = tk.Scrollbar(pageAbout, orient='vertical', command=txtAbout.yview)
txtAbout.insert(tk.END, text)
txtAbout['state'] = 'disabled'
txtAbout['yscrollcommand'] = ysAbout.set
ysAbout.grid(row=1, column=1)

btnBackAbout = tk.Button(pageAbout, text='Back', command=lambda:change_page(page1))
btnBackAbout.grid(row=2,column=0)

window.mainloop()