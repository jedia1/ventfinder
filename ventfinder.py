#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:11:53 2024

@author: jennadia
"""

import pandas as pd
import rasterio as rio
import numpy as np
import csv
import fiona
import os 

def create_shapefiles(mirova_csv, path_to_results, project_name, epsg_code, thermal_lon, thermal_lat, rctr_p):
    # make shapefile from MIROVA .csv
    df = pd.read_csv(mirova_csv, header=0, sep=',')
    ctr = (df['L_MIR'] + df['L_TIR']).to_numpy()
    rctr = ctr/np.amax(ctr)
    df['CTR'] = ctr
    df['Relative CTR'] = rctr
    columns = list(df.columns)
    crs = f'epsg:{epsg_code}'
    dtypes = []
    # the following loop is done so a datatype list can be constructed, even if the MIROVA team adds or subtracts columns from the .csv file 
    for i in df.dtypes:
        if i == 'object':
            dtypes.append('str')
        elif i == 'int64':
            dtypes.append('int')
        elif i == 'float64':
            dtypes.append('float')
        else:
            raise Exception(f'Datatype {i} not currently available. Current pandas datatypes handled are: object, float64, and int64.')
    schema = {'geometry': 'Polygon', 'properties': list(zip(columns, dtypes))}
    alerted_pixels_directory = f'{path_to_results}alerted_pixels_{project_name}'
    os.mkdir(alerted_pixels_directory)
    alerted_pixels_shapefile = alerted_pixels_directory + f'/alerted_pixels_{project_name}.shp'
    polyShp_alerted = fiona.open(alerted_pixels_shapefile, mode='w', driver='ESRI Shapefile', schema=schema, crs=crs)
    for i in range(df.shape[0]):
        x = df.LON[i]
        y = df.LAT[i]
        left_x = x - 375/2
        top_y = y + 375/2
        right_x = x + 375/2
        bottom_y = y - 375/2
        coords = [[(left_x, top_y), (right_x, top_y),
                         (right_x, top_y), (right_x, bottom_y),
                         (right_x, bottom_y), (left_x, bottom_y),
                         (left_x, bottom_y), (left_x, top_y)]]
        properties = dict(list(zip(columns, df.values[i])))
        geo_dict = {'geometry': {'type': 'Polygon', 
                    'coordinates': coords},
                    'properties': properties}
    
        polyShp_alerted.write(geo_dict)
    
    polyShp_alerted.close()
    
    # make shapefile for thermally thresholded pixels


def separate_clusters(index_tuples):
    """
    This function separates clusters of cells of interest in a numpy array. The 
    cells of interest are given by an array of tuples which represent indicies 
    in the numpy array. The array of tuples is iterated over. The function
    identifies all the cells that tocuh the first cell (represented by the 
    first tuple in index_tuples), and then iterates over a list of all the touching
    cells to identify unique cells that touch those cells. This process countinues
    until there are no more unique cells, and the cluster is thus identified.
    The function then continues iterating over index_tuples until it finds a 
    cells that has not yet been identified, and the clustering process begins 
    again. This continues until all index_tuples have been clustered. 
    

    Parameters
    ----------
    index_tuples : tuple
        Tuple containing a NumPy array of row indicies in its [0] index and  of column
        indicies in its [1] index. These row and column indicies represent
        cells of interest in a numpy array and are to be clustered.

    Returns
    -------
    groups : list
        List whose elements are lists of coordinates. Each list is a cluster of
        cells within the array of interest.

    """
    hot_pix = []
    for i in range(len(index_tuples[0])):
        hot_pix.append([index_tuples[0][i], index_tuples[1][i]])
        # restructures tuples list so each index in hot_pix is the [row, col]
        # coordinates of a cell in array of interest
    groups = [] # initialize list in which to store clusters of indicies
    n=0 # represents current number of clusters
    for count, pix in enumerate(hot_pix):
        bool_list_pix = [True if pix not in g else False for g in groups] 
        # checks if current cell (pixel) has been identified as part of a cluster already
        if count == 0: # for the first cell in hot_pix only
            groups.append([]) # appends an empty list to 'groups' list for 
            # storing the first cluster
            groups[n].append(pix) # appends first cell to the new list
            
        elif False in bool_list_pix: # pix in groups[-1]:
            continue # cell is already included in a previously identified cluster
            # this skips the remaining lines of code in the 'for' loop and advances
            # to the next cell in hot_pix
            
        else: # the current cell is not in any previously identified cluster.
            # new cluster must be created
            n += 1
            groups.append([]) # appends new empty list to 'groups' for next cluster
            groups[n].append(pix) # appends current pixel to new group
            
        for sub_pix in groups[n]: # iterates over the cells in the current cluster. List grows dynamically
            bool_list_subpix = [True if [sub_pix[0]+1, sub_pix[1]] not in g else False for g in groups] 
            # the above line checks if the cell ABOVE the current  has already been identified 
            if [sub_pix[0]+1, sub_pix[1]] in hot_pix and False not in bool_list_subpix: # [sub_pix[0]+1, sub_pix[1]] not in groups[n]:
            # i.e. if the cell above the current cell is in the hot_pix list, and has not yet been identified:
                groups[n].append([sub_pix[0]+1, sub_pix[1]])
            
            bool_list_subpix = [True if [sub_pix[0]-1, sub_pix[1]] not in g else False for g in groups]
            # the above line checks if the cell BELOW the current  has already been identified 
            if [sub_pix[0]-1, sub_pix[1]] in hot_pix and False not in bool_list_subpix: # [sub_pix[0]-1, sub_pix[1]] not in groups[n]:
                # i.e. if the cell below the current cell is in the hot_pix list, and has not yet been identified:
                groups[n].append([sub_pix[0]-1, sub_pix[1]])
                    
            bool_list_subpix = [True if [sub_pix[0], sub_pix[1]+1] not in g else False for g in groups]
            # the above line checks if the cell TO THE LEFT OF the current  has already been identified
            if [sub_pix[0], sub_pix[1]+1] in hot_pix and False not in bool_list_subpix: # [sub_pix[0], sub_pix[1]+1] not in groups[n]:
                # i.e. if the cell to the left of the current cell is in the hot_pix list, and has not yet been identified:
                groups[n].append([sub_pix[0], sub_pix[1]+1])

            bool_list_subpix = [True if [sub_pix[0], sub_pix[1]-1] not in g else False for g in groups]
            # the above line checks if the cell TO THE RIGHT OF the current  has already been identified
            if [sub_pix[0], sub_pix[1]-1] in hot_pix and False not in bool_list_subpix: # [sub_pix[0], sub_pix[1]-1] not in groups[n]:
                # i.e. if the cell to the right of the current cell is in the hot_pix list, and has not yet been identified:
                groups[n].append([sub_pix[0], sub_pix[1]-1])
            
    return groups


def cluster_id_and_relative_radiance(lat_array, lon_array, pixel_resolution, radiance_array, threshold):
    """
    This function carries out the following operations:
    1) Determines the lat/lon extent of the alerted MIROVA pixels and creates
    meshgrids for both lat and lon (y_mesh and x_mesh, respectively)
    2) Identifies the indicies of radiances above a specified theshold (default:
    relative radiance = 0.5 and higher) and uses the separate_clusters function 
    to cluster them
    3) Renormalizes the radiances within each cluster and once again identifies 
    indicies above the specified threshold, and uses the separate_clusters 
    function to trim the clusters

    Parameters
    ----------
    lat_array : array-like
        One-dimensional series containing latitudes of alerted MIROVA pixels
    lon_array : array-like
        One-dimensional series containing longitudes of alerted MIROVA pixels
    pixel_resolution : float or int
        Resolution of the MIROVA pixels
    radiance_array : array-like
        One dimensional array containing the sum of middle infrared radiance and
        thermal infrared radiance for each alerted MIROVA pixel
    threshold : float, optional
        The normalized radiance at or above which to consider the MIROVA pixel. 
        The default is 0.5.

    Returns
    -------
    groups : list
        List whose elements are lists of indices. Each sub-list represents a cluster of
        hot MIROVA pixels within the radiance array
    x_mesh : numpy array
        Two-dimensional numpy array containing the longitutdes which correspond
        to the pixels in grid_rad_relative and grid_rad_relative_prime 
    y_mesh : numpy array
        Two-dimensional numpy array containing the latitutdes which correspond
        to the pixels in grid_rad_relative and grid_rad_relative_prime 
    grid_rad_relative_prime : numpy array
        Grid containng relevant pixels and their re-normalized (within cluster)
        radiance values. The indices of the values correspond to the indicies
        of their latitudes and longitudes in y_mesh and x_mesh, respectively.

    """
    # renaming some variables for brevity
    resolution = pixel_resolution
    lat = lat_array
    lon = lon_array
    total_rad = radiance_array
    
    # first, have to get the lat+lon extent to build the meshgrid
    min_lat = np.amin(lat)
    max_lat = np.amax(lat)
    min_lon = np.amin(lon)
    max_lon = np.amax(lon)
    xlon = np.arange(min_lon, max_lon+resolution, resolution)
    ylat = np.arange(max_lat, min_lat-resolution, -resolution)
    
    # create 2d arrays of latitude and longitude (note: for lat, every column in
    # a single row will have the same value, and for lon, every row in a single
    # column will have the same value)
    x_mesh, y_mesh = np.meshgrid(xlon, ylat)
    # initialze grid with same dimensions as lat and lon grids (y_mesh and 
    # x_mesh, respectively)
    grid = np.zeros(x_mesh.shape)
    # each radianc will correspond to the lat and lon at the same indicies in 
    # y_mesh and x_mesh, respectively
    
    for i, rad in enumerate(total_rad): # iterate over 1d radiance array
        # get latitude and longitude correspoding to that radiance
        current_lat = lat[i]
        current_lon = lon[i]
        # get row and column indicies from lat and lon 1d arrays to determine 
        # where in the grid the radiance will go
        col = np.where(xlon == current_lon)
        row = np.where(ylat == current_lat)
        grid[row, col] = rad # set grid at row and column to radiance
    grid_rad_relative = grid/np.amax(grid) # normalize radiances to 1
    # find indicies where normalized radiances are at or above threshold
    hot_pix_nonzero_tp = np.where(grid_rad_relative >= threshold)
    # run separate_clusters on cells identifies by the above tuples
    groups_first = separate_clusters(hot_pix_nonzero_tp)
    # intialize renormalized grid
    grid_rad_relative_prime = np.zeros(grid_rad_relative.shape)
    for group in groups_first: # iterate over the list of clusters returned by 
    # separate_pixels
        # intialize 1d array of radiances for the cluster
        rad_list = np.zeros(len(group))
        for count, coord in enumerate(group): # iterate over coordinates within
        # the current cluster
            rad_list[count] = grid_rad_relative[coord[0], coord[1]] # insert 
            # radiances from normalized grid into array
        rad_list_norm = rad_list/np.amax(rad_list) # re-normalize radiances in 
        # cluster to 1
        for count, coord in enumerate(group):
            # insert re-normalized radiances into approriate indcies in 
            # renormalized grid
            grid_rad_relative_prime[coord[0], coord[1]] = rad_list_norm[count] 
        
        # find indicies where re-normalized radiances are at or above threshold
        hot_pix_tp = np.where(grid_rad_relative_prime >= threshold)
        # run separate_clusters on cells identifies by the above tuples. The 
        # number of clusters identified should be the same as the first run,
        # but the clusters may contain less cells
        groups = separate_clusters(hot_pix_tp)

    
    return groups, x_mesh, y_mesh, grid_rad_relative_prime

def highest_in_cluster(dem_elevations, dem_lat, dem_lon, groups, x_mesh, 
                               y_mesh, resolution, grid):
    """
    This function finds the highest MIROVA pixel with each pixel cluster. It 
    averages the DEM elevations within each MIROVA pixel of interest. The pixel
    with the highest averaged elevation in its cluster is noted and its lat and
    lon coordinates recorded.

    Parameters
    ----------
    dem_elevations : numpy array
        Elevations extracted from DEM
    dem_lat : numpy array
        Latitudes extracted from the DEM
    dem_lon : numpy array
        Longitudes extracted from the DEM
    groups : list
        List whose elements are lists of coordinates representing clusters
    x_mesh : numpy array
        Two dimensional array of longitudes corresponding to the center of MIROVA 
        pixels of interest and their radiances in grid
    y_mesh : numpy array
        Two dimensional array of latitudes corresponding to the center of MIROVA 
        pixels of interest and their radiances in grid
    resolution : float or int
        Resolution of the MIROVA pixels
    grid : numpy array
        Two dimensional grid of radiances. The indicies in the grid correspond
        to latitudes and longitudes in y_mesh and x_mesh, respectively

    Returns
    -------
    coords : list
        list whose elements are lists containing the latitude, longitude, and
        average elevation of the highest pixel in a cluster

    """
    pix_avg_elevations = np.zeros(x_mesh.shape) # initialize array to store 
    # average elevations. Same dimensions as x_mesh, y_mesh, and grid with 
    # corresponding indicies
    coords = []
    for cluster in groups: # iterate over list of clusters
        elev = [] # empty list to which elevations will be appended
        if len(cluster) >= 3: # exlcuded clusters that have less than 3 pixels
            for idx in cluster: # iterate over indicies within the cluster
                pixel_lat = y_mesh[idx[0], idx[1]] # lat of pixel center
                pixel_lon = x_mesh[idx[0], idx[1]] # lon of pixel center
                
                # get coordinates of top left of pixel
                topleft_lat = pixel_lat + resolution/2
                topleft_lon = pixel_lon - resolution/2
                
                # get coordinates of bottom right of pixel
                bottomright_lat = pixel_lat - resolution/2
                bottomright_lon = pixel_lon + resolution/2
                
                # find indicies where MIROVA pixel and DEM pixels overlap
                lat_diff_top = abs(dem_lat - topleft_lat)
                lon_diff_top = abs(dem_lon - topleft_lon)
                near_zero_row_top = np.argmin(lat_diff_top[:,0])
                near_zero_col_top = np.argmin(lon_diff_top[0,:])
                lat_diff_bottom = abs(dem_lat - bottomright_lat)
                lon_diff_bottom = abs(dem_lon - bottomright_lon)
                near_zero_row_bottom = np.argmin(lat_diff_bottom[:,0])
                near_zero_col_bottom = np.argmin(lon_diff_bottom[0,:])
                
                # get the average elevation of the MIROVA pixel these indicies
                pixel_elevations = dem_elevations[near_zero_row_top:near_zero_row_bottom, near_zero_col_top:near_zero_col_bottom]
                pixel_elevation_mean = np.mean(pixel_elevations)        
                lat_idx = np.where(y_mesh[:,0]==pixel_lat)
                lon_idx = np.where(x_mesh[0,:]==pixel_lon)
                pix_avg_elevations[lat_idx, lon_idx] = pixel_elevation_mean
                elev.append(pixel_elevation_mean)
            
            max_elev = max(elev)
            max_elev_idx = np.where(np.array(elev) == max_elev)[0][0]
            idx = cluster[max_elev_idx]
            lat = y_mesh[idx[0], idx[1]]
            lon = x_mesh[idx[0], idx[1]]
            coords.append([lat, lon, max_elev])
    
    return coords

def mask_bounds(mask_layer):
    mask_raster = rio.open(mask_layer)
    rows = mask_raster.shape[0]
    cols = mask_raster.shape[1]
    min_x, max_y = rio.transform.xy(mask_raster.transform, 0, 0)
    max_x, min_y = rio.transform.xy(mask_raster.transform, rows, cols)
    
    return min_x, min_y, max_x, max_y
            
def run_ventfinder(mirova_csv, dem, path_to_results, project_name, threshold=0.5, mask=None):
    """
    Reads the input files, calls cluster_id_and_normalization and highest_in_cluster,
    and writes a .csv file with the latitude and longitude coordinates and 
    average elevation of the highest MIROVA pixel in each cluster.

    Parameters
    ----------
    mirova_csv : string
        Path to .csv with alerted pixel information
    dem : string
        Path to DEM
    path_to_results : string
        path to folder where .csv output will be written

    Returns
    -------
    None.

    """
    if path_to_results[-1] != '/':
        path_to_results = path_to_results + '/'
    
    df = pd.read_csv(mirova_csv)
    if mask is not None:
        min_x, min_y, max_x, max_y = mask_bounds(mask)
        keep_rows = [i for i in range(len(df)) if (df['LON'][i] <= min_x or df['LON'][i] >= max_x) and (df['LAT'][i] <= min_y or df['LAT'][i] >= max_y)]
        df = df.iloc[keep_rows]
        df.to_csv(path_to_results + project_name + 'masked_input.csv', index=False)
    
    resolution = df['RES'][0]
    lat = (df['LAT']).to_numpy()
    lon = (df['LON']).to_numpy()
    l_mir = (df['L_MIR']).to_numpy()
    l_tir = (df['L_TIR']).to_numpy()
    # add MIR and TIR radiances
    combo = l_mir + l_tir
    
    dem = rio.open(dem)
    elevations = dem.read(1)
    dem_res = dem.meta['transform'][0]
    height = elevations.shape[0]
    width = elevations.shape[1]
    cols, rows = np.meshgrid(np.arange(width), np.arange(height))
    x, y = rio.transform.xy(dem.transform, rows, cols)
    dem_lat = np.array(y) - dem_res/2 # this puts the coordinates in the lower left corner of the pixel, matching the DEM
    dem_lon = np.array(x) - dem_res/2
    dem.close()
    
    groups, x_mesh, y_mesh, grid_rad_relative = cluster_id_and_relative_radiance(lat, lon, resolution, combo, threshold=threshold)
    thermal_latitudes = []
    thermal_longitudes = []
    rads_prime = []
    for cluster in groups:
        for coords in cluster:
            thermal_latitude = y_mesh[coords[0], coords[1]]
            thermal_latitudes.append(thermal_latitude)
            thermal_longitude = x_mesh[coords[0], coords[1]]
            thermal_longitudes.append(thermal_longitude)
            rctr_p = grid_rad_relative[coords[0], coords[1]]
            rads_prime.append(rctr_p)
            thermal_longitudes.append(thermal_longitude)

    
    coords = highest_in_cluster(elevations, dem_lat, dem_lon, 
                                        groups, x_mesh, y_mesh, resolution, grid_rad_relative)
    
    fields = ['LAT', 'LON', 'Elevation']
    outfile = path_to_results + project_name + '_selected_pixels.csv'
    with open(outfile, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(coords)
        

