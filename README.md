# Ventfinder

The purpose of this code is to localize effusive volcanic vents at the start of an eruption using data collected by the Visible Infrared Imaging Radiometer Suite (VIIRS) and processed by the Middle Infrared Observations of Volanic Activity (MIROVA) algorithm (Coppola et al., 2016, Coppola et al., 2020, Campus et al., 2022). It is optimized for the VIIRS 375 m resolution imaging bands in the thermal and infrared ranges. VIIRS 375 data is obtained from the MIROVA 
team in a .csv file, which the Ventfinder reads. A DEM for the volcano of interest is also required for the Ventfinder. 

The Ventfinder works by adding the middle infrared (MIR) and thermal infrared (TIR) radiances together for each MIROVA-alerted pixel. The resulting value is the combined thermal radiance (CTR). The CTR values are normalized to the largest CTR value; the normalized value is called the relative CTR or rCTR value. The ventfinder then delineates clusters of pixels with an rCTR value greater than or equal to a threshold. The default thershold is 0.5, but this may be 
changed by the user. Then, it re-normalizes rCTR to the highest rCTR value in each cluster; this value is called rCTR'. Pixels with rCTR' less than the threshold are dropped from their clusters and no longer considered. Next, the average elevation is calculated for each remaining pixel (it is an average elevation because the DEM resolution is likely much finer that the MIROVA pixel resoluion). For each cluster, the pixel with the highest average elevation is 
selected, and the selected pixels' center UTM coordiantes and average elevation are written to a .csv file. These selected pixels are presumed likliest to contain an effusive vent.

This is distributed with no guarantee that it can accurately predict teh eruptive vent location.

This code was written with python 3.11 and uses the packages NumPy, pandas, rasterio, fiona. The GUI was built using tkinter.

References:

Campus, A., Laiolo, M., Massimetti, F., & Coppola, D. (2022). The transition from MODIS to VIIRS for global volcano thermal monitoring. Sensors, 22(5), 1713.

Coppola, D., Laiolo, M., Cigolini, C., Delle Donne, D., & Ripepe, M. (2016). Enhanced volcanic hot-spot detection using MODIS IR data: results from the MIROVA system.

Coppola, D., Laiolo, M., Cigolini, C., Massimetti, F., Delle Donne, D., Ripepe, M., ... & William, R. (2020). Thermal remote sensing for global volcano monitoring: experiences from the MIROVA system. Frontiers in Earth Science, 7, 362.
