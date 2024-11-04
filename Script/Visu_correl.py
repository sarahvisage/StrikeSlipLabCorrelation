#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:05:23 2024

@author: sarahvisage
"""

import numpy as np
from scipy.ndimage import median_filter
import pandas as pd
import os
import tifffile as tiff
import matplotlib.pyplot as plt
import yaml

from plot_save_correl_function import plot_save_correl_function, plot_profil_3D, plot_profil_vertical


''''''''''''''''''''''''' DEBUT DE LA ZONE DE CHOIX '''''''''''''''''''''''''''
# %%

NumExp = 'E573'  # Choose the name of the experience to view

''' PATH FILE INFO ''' # les chemins sont relatifs, si l'arborescence des dossiers est respecté pas besoin de les changer

      
if os.name == 'posix':
    path_base = '../'
elif os.name == 'nt':    
    path_base = '..\\'
    
    
file_info_name = 'param_correl.xlsx'

file_info = pd.read_excel(f"{path_base}{file_info_name}", sheet_name='param_correl')

''' DEBUT DE LA BOUCLE ''' #renseigner les numéros de la première et de la dernière frame dans le fichier excel 'param_correl.xlsx'



#%%

with open(path_base + 'parameters.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Extraction et assignation les paramètres
NumExp = config['general']['NumExp']
scale = config['general']['scale']
VisibilitePlot = config['general']['VisibilitePlot']
Folder_NameOut = config['general']['Folder_NameOut']

first_frame = config['frames']['first_frame']
last_frame = config['frames']['last_frame']

if first_frame is None:

    first_frame = file_info.loc[file_info['Exp'] == NumExp, 'debut_expe'].values[0] 
    last_frame = file_info.loc[file_info['Exp'] == NumExp, 'fin_expe'].values[0]

Filtre = config['filtre']['Filtre']

DepNorm = config['components']['DepNorm']
UxParallel = config['components']['UxParallel']
UyPerp = config['components']['UyPerp']
Shear = config['components']['Shear']
SecondInv = config['components']['SecondInv']
Curl = config['components']['Curl']
Divergence = config['components']['Divergence']
seisme = config['components']['seisme']

profilVertical = config['profil']['profilVertical']
if profilVertical:
    profilV_1_mm = config['profil']['profilV_1_mm']
    profilV_2_mm = config['profil']['profilV_2_mm']
    profilV_3_mm = config['profil']['profilV_3_mm']
    
profil3D = config['profil']['profil3D']
if profil3D:
    profil1 = config['profil']['profil1']
    profil2 = config['profil']['profil2']
    profil3 = config['profil']['profil3']
    NbProfil = config['profil']['NbProfil']
    PasProfil = config['profil']['PasProfil']

Quivers = config['other']['Quivers']
riedels = config['other']['riedels']

Zoom = config['visualization']['Zoom']
ymin_mm = config['visualization']['ymin_mm']
ymax_mm = config['visualization']['ymax_mm']
xmin_mm = config['visualization']['xmin_mm']
xmax_mm = config['visualization']['xmax_mm']

# %%

DD = file_info.loc[file_info['Exp'] == NumExp, 'stock'].values[0] # Info sur la localisation des données de corrélation, 
                                                                  # mettre le nom du disque dur dans le fichier excel 'param_correl.xlsx'
                                                                  # si les correl sont en local dans le dossier 'Correlation_experience' 
                                                                  # de l'arborescence : mettre 'Local' dans le fichier excel 

# Pas besoin de changer les chemins, que ce soit sur Linux, Mac ou Windows
if DD == 'Local':
    if os.name == 'posix':
        Correl_path = f"{path_base}Correlation_experience/{NumExp}/"
    elif os.name == 'nt':
        Correl_path = f"{path_base}Correlation_experience\\{NumExp}\\"
else:
    if os.name == 'posix':
        Correl_path = f"/media/sarah/{DD}/{NumExp}/"
    elif os.name == 'nt':
        Correl_path = f"{DD}:\\{NumExp}\\"
        
''' SENS PHOTO '''
sens = file_info.loc[file_info['Exp'] == NumExp, 'sens'].values[0]


''' A METTRE A JOUR '''
# if seisme == 1:
#     seisme_struct = loadmat(f"{cheminrecording}/Figures/{NumExp}/catalogue/seisme.mat")
#     seisme = seisme_struct['seisme'][0, :]

for j in range(first_frame , last_frame + 1):
    
    plt.close('all')
    
    FolderNameFrame = f"{Correl_path}frame{j}/"
    
    print(f"frame{j}")
    
    Ux = tiff.imread(f"{FolderNameFrame}Px1_Num6_DeZoom1_LeChantier.tif")
    Uy = tiff.imread(f"{FolderNameFrame}Px2_Num6_DeZoom1_LeChantier.tif")
    

    resolution = file_info.loc[file_info['Exp'] == NumExp, 'Resolution (pxl/mm)'].values[0] # pxl/mm

    if scale == 'millimetre':
        Ux = Ux / resolution
        Uy = Uy / resolution
    elif scale == 'micrometre':
        Ux = (Ux / resolution) * 1e3
        Uy = (Uy / resolution) * 1e3

    nx, ny = Ux.shape[1], Uy.shape[0]

    AxisX = np.arange(1, nx + 1) / resolution
    AxisY = np.arange(1, ny + 1) / resolution

    if Zoom == 0:
        ymin_mm = 0
        ymax_mm = AxisY[-1]
        xmin_mm = 0
        xmax_mm = AxisX[-1]

    ymin = np.argmin(np.abs(AxisY - ymin_mm))
    ymax = np.argmin(np.abs(AxisY - ymax_mm))
    xmin = np.argmin(np.abs(AxisX - xmin_mm))
    xmax = np.argmin(np.abs(AxisX - xmax_mm))
    

    dx = AxisX[1] - AxisX[0]
    dy = AxisY[1] - AxisY[0]

    AxisXZ = AxisX[xmin:xmax]
    AxisYZ = AxisY[ymin:ymax]

    UxZoom = Ux[ymin:ymax, xmin:xmax]
    UyZoom = Uy[ymin:ymax, xmin:xmax]
    
    if profil3D == 1:
        profil1 = np.argmin(np.abs(AxisYZ - profil1))
        profil2 = np.argmin(np.abs(AxisYZ - profil2))
        profil3 = np.argmin(np.abs(AxisXZ - profil3))
        
    if profilVertical == 1:
        profilV_1 = np.argmin(np.abs(AxisXZ - profilV_1_mm))
        profilV_2 = np.argmin(np.abs(AxisXZ - profilV_2_mm))
        profilV_3 = np.argmin(np.abs(AxisXZ - profilV_3_mm))

    nyZ, nxZ = UxZoom.shape

    if Filtre == 1:
        UxZoom = median_filter(UxZoom, size=(10, 10))
        UyZoom = median_filter(UyZoom, size=(10, 10))

    # DERIVEES
    if Shear == 1 or SecondInv == 1 or Curl == 1 or Divergence == 1:
        dUxdx = np.zeros_like(UxZoom)
        dUxdy = np.zeros_like(UxZoom)
        dUydy = np.zeros_like(UyZoom)
        dUydx = np.zeros_like(UyZoom)

        for r in range(1, nxZ - 1):
            dUxdx[:, r] = (UxZoom[:, r + 1] - UxZoom[:, r - 1]) / (2 * dx)

        for i in range(1, nyZ - 1):
            dUxdy[i, :] = (UxZoom[i + 1, :] - UxZoom[i - 1, :]) / (2 * dy)

        for r in range(1, nyZ - 1):
            dUydy[r, :] = (UyZoom[r + 1, :] - UyZoom[r - 1, :]) / (2 * dy)

        for i in range(1, nxZ - 1):
            dUydx[:, i] = (UyZoom[:, i + 1] - UyZoom[:, i - 1]) / (2 * dx)

    
    if DepNorm == 1:
        Type = 'Displacement'
        if sens == 1:
            UxZoom = np.flipud(-UxZoom)
            UyZoom = np.flipud(-UyZoom)
        DeplZ = np.sqrt(UxZoom ** 2 + UyZoom ** 2)
        
        if scale == 'millimetre':
            Unite = ' [mm]'
        elif scale == 'micrometre':
            Unite = ' [micromètres]'
    
        LimMin = file_info.loc[file_info['Exp'] == NumExp, 'Limite_Deplacement_Min'].values[0]
        LimMax = file_info.loc[file_info['Exp'] == NumExp, 'Limite_Deplacement_Max'].values[0]
        
        plot_save_correl_function(VisibilitePlot, DeplZ, LimMin, LimMax, Type, Unite, j, 
             xmin_mm, xmax_mm, ymin_mm, ymax_mm, NumExp, Folder_NameOut, path_base, 
             Quivers, Ux, Uy, AxisX, AxisY, scale)
        
        if profil3D:
            plot_profil_3D(AxisX, AxisY, DeplZ, LimMin, LimMax, Type, Unite,
                j, xmin_mm, xmax_mm, ymin_mm, ymax_mm, path_base, NumExp, NbProfil,
                PasProfil, profil1, profil2, profil3, Folder_NameOut, VisibilitePlot)
            
        if profilVertical:
            plot_profil_vertical(AxisXZ, AxisYZ, DeplZ, LimMin, LimMax, Type, Unite,
                            j, xmin_mm, xmax_mm, ymin_mm, ymax_mm, path_base, NumExp,
                            profilV_1_mm, profilV_2_mm, profilV_3_mm, profilV_1, 
                            profilV_2, profilV_3, Folder_NameOut, VisibilitePlot, scale)
        
        pass
    
    if UxParallel == 1:
        Type = 'Parallel_Displacement'
        if sens == 1:
            UxZoom = np.flipud(-UxZoom)
            
        
        
        if scale == 'millimetre':
            Unite = ' [mm]'
        elif scale == 'micrometre':
            Unite = ' [micromètres]'
    
        LimMin = file_info.loc[file_info['Exp'] == NumExp, 'Limite_Deplacement_Min'].values[0]
        LimMax = file_info.loc[file_info['Exp'] == NumExp, 'Limite_Deplacement_Max'].values[0]
        
        plot_save_correl_function(VisibilitePlot, UxZoom, LimMin, LimMax, Type, Unite, j, 
             xmin_mm, xmax_mm, ymin_mm, ymax_mm, NumExp, Folder_NameOut, path_base, 
             Quivers, Ux, Uy, AxisX, AxisY, scale)
        
        if profil3D:
            plot_profil_3D(AxisX, AxisY, Ux, LimMin, LimMax, Type, Unite,
                j, xmin_mm, xmax_mm, ymin_mm, ymax_mm, path_base, NumExp, NbProfil,
                PasProfil, profil1, profil2, profil3, Folder_NameOut, VisibilitePlot)
            
        if profilVertical:
            plot_profil_vertical(AxisXZ, AxisYZ, UxZoom, LimMin, LimMax, Type, Unite,
                            j, xmin_mm, xmax_mm, ymin_mm, ymax_mm, path_base, NumExp,
                            profilV_1_mm, profilV_2_mm, profilV_3_mm, profilV_1, 
                            profilV_2, profilV_3, Folder_NameOut, VisibilitePlot, scale)
        
        pass
    
    if UyPerp == 1:
        Type = 'Perpendiculaire_Displacement'
        if sens == 1:
            UyZoom = np.flipud(-UyZoom)
            
        
        
        if scale == 'millimetre':
            Unite = ' [mm]'
        elif scale == 'micrometre':
            Unite = ' [micromètres]'
    
        LimMin = file_info.loc[file_info['Exp'] == NumExp, 'Limite_Deplacement_Min'].values[0]
        LimMax = file_info.loc[file_info['Exp'] == NumExp, 'Limite_Deplacement_Max'].values[0]
        
        plot_save_correl_function(VisibilitePlot, UyZoom, LimMin, LimMax, Type, Unite, j, 
             xmin_mm, xmax_mm, ymin_mm, ymax_mm, NumExp, Folder_NameOut, path_base, 
             Quivers, Ux, Uy, AxisX, AxisY, scale)
        
        if profil3D:
            plot_profil_3D(AxisX, AxisY, Uy, LimMin, LimMax, Type, Unite,
                j, xmin_mm, xmax_mm, ymin_mm, ymax_mm, path_base, NumExp, NbProfil,
                PasProfil, profil1, profil2, profil3, Folder_NameOut, VisibilitePlot)
        
        if profilVertical:
            plot_profil_vertical(AxisXZ, AxisYZ, UyZoom, LimMin, LimMax, Type, Unite,
                            j, xmin_mm, xmax_mm, ymin_mm, ymax_mm, path_base, NumExp,
                            profilV_1_mm, profilV_2_mm, profilV_3_mm, profilV_1, 
                            profilV_2, profilV_3, Folder_NameOut, VisibilitePlot, scale)
        
        pass
    
    if Shear == 1:
        Type = 'Shear_strain'
            
        shear = 1/2*(dUxdy + dUydx);
        
        if scale == 'millimetre':
            Unite = ' [mm]'
        elif scale == 'micrometre':
            Unite = ' [micromètres]'
    
        LimMin = np.min(shear)
        LimMax = np.max(shear)
        
        plot_save_correl_function(VisibilitePlot, shear, LimMin, LimMax, Type, Unite, j, 
             xmin_mm, xmax_mm, ymin_mm, ymax_mm, NumExp, Folder_NameOut, path_base, 
             Quivers, Ux, Uy, AxisX, AxisY, scale)
        
        if profilVertical:
            plot_profil_vertical(AxisXZ, AxisYZ, shear, LimMin, LimMax, Type, Unite,
                            j, xmin_mm, xmax_mm, ymin_mm, ymax_mm, path_base, NumExp,
                            profilV_1_mm, profilV_2_mm, profilV_3_mm, profilV_1, 
                            profilV_2, profilV_3, Folder_NameOut, VisibilitePlot, scale)
        
        pass
    
    if Curl == 1:
        Type = 'Curl'
            
        curl = dUydx - dUxdy;
        
        if scale == 'millimetre':
            Unite = ' [mm]'
        elif scale == 'micrometre':
            Unite = ' [micromètres]'
    
        LimMin = np.min(curl)
        LimMax = np.max(curl)
        
        plot_save_correl_function(VisibilitePlot, curl, LimMin, LimMax, Type, Unite, j, 
             xmin_mm, xmax_mm, ymin_mm, ymax_mm, NumExp, Folder_NameOut, path_base, 
             Quivers, Ux, Uy, AxisX, AxisY, scale)
        
        if profilVertical:
            plot_profil_vertical(AxisXZ, AxisYZ, curl, LimMin, LimMax, Type, Unite,
                            j, xmin_mm, xmax_mm, ymin_mm, ymax_mm, path_base, NumExp,
                            profilV_1_mm, profilV_2_mm, profilV_3_mm, profilV_1, 
                            profilV_2, profilV_3, Folder_NameOut, VisibilitePlot, scale)
        
        pass
    
    if Divergence == 1:
        Type = 'Divergence'
            
        div = dUxdx + dUydy;
        
        if scale == 'millimetre':
            Unite = ' [mm]'
        elif scale == 'micrometre':
            Unite = ' [micromètres]'
    
        LimMin = np.min(div)
        LimMax = np.max(div)  
    
        plot_save_correl_function(VisibilitePlot, div, LimMin, LimMax, Type, Unite, j, 
             xmin_mm, xmax_mm, ymin_mm, ymax_mm, NumExp, Folder_NameOut, path_base, 
             Quivers, Ux, Uy, AxisX, AxisY, scale)
        
        if profilVertical:
            plot_profil_vertical(AxisXZ, AxisYZ, div, LimMin, LimMax, Type, Unite,
                            j, xmin_mm, xmax_mm, ymin_mm, ymax_mm, path_base, NumExp,
                            profilV_1_mm, profilV_2_mm, profilV_3_mm, profilV_1, 
                            profilV_2, profilV_3, Folder_NameOut, VisibilitePlot, scale)
        
        pass

    if SecondInv == 1:
        Type = 'Second_Invariant'
            
        Inv2 = 1/2*(dUxdx*dUydy) - (dUxdy*dUydx);
                    
        
        if scale == 'millimetre':
            Unite = ' [mm]'
        elif scale == 'micrometre':
            Unite = ' [micromètres]'
    
        LimMin = np.min(Inv2)
        LimMax = np.max(Inv2)
        
        plot_save_correl_function(VisibilitePlot, UyZoom, LimMin, LimMax, Type, Unite, j, 
             xmin_mm, xmax_mm, ymin_mm, ymax_mm, NumExp, Folder_NameOut, path_base, 
             Quivers, Ux, Uy, AxisX, AxisY, scale)
        
        if profilVertical:
            plot_profil_vertical(AxisXZ, AxisYZ, Inv2, LimMin, LimMax, Type, Unite,
                            j, xmin_mm, xmax_mm, ymin_mm, ymax_mm, path_base, NumExp,
                            profilV_1_mm, profilV_2_mm, profilV_3_mm, profilV_1, 
                            profilV_2, profilV_3, Folder_NameOut, VisibilitePlot, scale)
        
        pass
