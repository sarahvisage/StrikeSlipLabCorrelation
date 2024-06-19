#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 14:58:53 2024

@author: sarahvisage
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from cmcrameri import cm
from scipy.ndimage import uniform_filter1d
import pdb


def plot_profil_vertical(AxisXZ, AxisYZ, plot, LimMin, LimMax, Type, Unite,
                j, xmin_mm, xmax_mm, ymin_mm, ymax_mm, path_base, NumExp,
                profilV_1_mm, profilV_2_mm, profilV_3_mm, profilV_1, profilV_2, 
                profilV_3, Dossier, VisibilitePlot, scale):
    
    if VisibilitePlot == 0:
        plt.ioff()  # Disable interactive mode to hide the plot
    
    label1 = 'profil ' + str(profilV_1_mm) + 'mm'
    label2 = 'profil ' + str(profilV_2_mm) + 'mm'
    label3 = 'profil ' + str(profilV_3_mm) + 'mm'
    
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={'width_ratios': [1, 1.3]})
    
    # Premier sous-graphe
    ax1.plot(AxisYZ, plot[:,profilV_1], color='#77AC30', linewidth=3, label=label1)
    ax1.plot(AxisYZ, plot[:,profilV_2], color='#0072BD', linewidth=3, label=label2)
    ax1.plot(AxisYZ, plot[:,profilV_3], color='#A2142F', linewidth=3, label=label3)
    ax1.legend()
    ax1.set_xlabel('Axis Y')
    ax1.set_ylabel(Type)
    ax1.set_title('Profiles Plot')
    
    # Deuxième sous-graphe
    im = ax2.imshow(plot, aspect='equal', extent=(xmin_mm, xmax_mm, ymin_mm, ymax_mm), cmap=cm.vik, origin='lower')
    ax2.set_xlabel('x [mm]')
    ax2.set_ylabel('y [mm]')
    ax2.tick_params(axis='both', labelsize=10)
    ax2.set_aspect(aspect=1)
    ax2.invert_yaxis()
    ax2.annotate('', xy=(xmin_mm + 120, ymax_mm - 50), xytext=(xmin_mm + 30, ymax_mm - 50),
            arrowprops={"width":1.5,"headwidth":5,'headlength':5, 'color':'k'})
    
    if scale == 'micrometre':
        displacement_text = f'total displacement = {j*0.025:.2f} mm'
    else:
        displacement_text = f'total displacement = {j*0.5:.2f} mm'
    
    ax2.text(xmin_mm, ymin_mm - 10, displacement_text, color='k', fontsize=12)
    
    cbar = plt.colorbar(im, ax=ax2, orientation='vertical', shrink=0.89)#,  location='left', shrink=0.85)
    cbar.set_label(f'{Type} {Unite}', fontsize=15)
    
    visuprof1 = np.ones(plot.shape[0])*profilV_1_mm
    visuprof2 = np.ones(plot.shape[0])*profilV_2_mm
    visuprof3 = np.ones(plot.shape[0])*profilV_3_mm
    
    ax2.plot(visuprof1, AxisYZ, color='#77AC30', linewidth=2, label=label1)
    ax2.plot(visuprof2, AxisYZ, color='#0072BD', linewidth=2, label=label2)
    ax2.plot(visuprof3, AxisYZ, color='#A2142F', linewidth=2, label=label3)
 
    plt.tight_layout()
    
    # if VisibilitePlot == 1:
    #     plt.show()
    
    
    save_dir = os.path.join(path_base, 'Figures', NumExp, 'profil_2D')
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.join(save_dir, 'frame-' + f'{j:.0f}.png')
    plt.savefig(filename, dpi=150, bbox_inches='tight')
   
    

def plot_profil_3D(AxisX, AxisY, Depl, LimMin, LimMax, Type, Unite,
                j, xmin_mm, xmax_mm, ymin_mm, ymax_mm, cheminbase, NumExp, NbProfil,
                PasProfil, profil1, profil2, profil3, Dossier, VisibilitePlot):

    if VisibilitePlot == 0:
        plt.ioff()  # Disable interactive mode to hide the plot
    
    plt.figure()
    plt.imshow(Depl, extent=[AxisX.min(), AxisX.max(), AxisY.min(), AxisY.max()], origin='lower', aspect='auto')
    plt.colorbar(label=f'{Type} {Unite}')
    plt.xlim([xmin_mm, xmax_mm])
    plt.ylim([ymin_mm, ymax_mm])
    plt.gca().invert_yaxis()
    plt.title('Select two points with mouse')
    
    # Using ginput to select two points
    points = plt.ginput(2)
    plt.close()

    Xa, Ya = points[0]
    Xb, Yb = points[1]
    

    a = (Yb - Ya) / (Xb - Xa)

    ProfilDep = np.zeros((int((1 + (NbProfil / PasProfil))), PasProfil))
    
    for i in range(1, NbProfil + 1, PasProfil):
        Xaprim = Xa + 1 * i
        Yaprim = (-1 / a) * Xaprim + (Ya + (1 / a) * Xa)

        Xbprim = Xb + 1 * i
        Ybprim = (-1 / a) * Xbprim + (Yb + (1 / a) * Xb)

        LAB = np.sqrt((Xbprim - Xaprim) ** 2 + (Ybprim - Yaprim) ** 2)
        largeur = max(AxisX)
        longueur = max(AxisY)
        nc = len(AxisX)
        nl = len(AxisY)
        pasx = largeur / (nc - 1)
        pasy = longueur / (nl - 1)
        pascoupe = 0.8 * min(pasx, pasy)
        ncoupe = 1 + (LAB / pascoupe)
        AB = np.ones(int(round(ncoupe)))

        Pxl = []
        Pyc = []      

        for k in range(int(ncoupe)):
            alpha = (k - 1) / (ncoupe - 1)
            Px = Xbprim * alpha + Xaprim * (1 - alpha)
            Py = Ybprim * alpha + Yaprim * (1 - alpha)

            Pxlk = round(Px / pasx + 1)
            Pyck = round(Py / pasy + 1)
            
            pdb.set_trace()

            # Ensure the indices are within bounds
            if 0 <= Pxlk < Depl.shape[1] and 0 <= Pyck < Depl.shape[0]:
                Pxl.append(Pxlk)
                Pyc.append(Pyck)
                ProfilDep[k, i] = Depl[Pyck, Pxlk]
            else:
                print(f"Skipping out-of-bounds indices Pxlk: {Pxlk}, Pyck: {Pyck}")
            

        hyP = AxisY[np.array(Pyc)]

        # Plotting logic
        # plt.plot(AxisX[np.array(Pxl)], AxisY[np.array(Pyc)], 'k')
        if i == profil1:
            plt.plot(AxisX[np.array(Pxl)], AxisY[np.array(Pyc)], color='#77AC30', linewidth=3)
        if i == profil2:
            plt.plot(AxisX[np.array(Pxl)], AxisY[np.array(Pyc)], color='#0072BD', linewidth=3)
        if i == profil3:
            plt.plot(AxisX[np.array(Pxl)], AxisY[np.array(Pyc)], color='#A2142F', linewidth=3)

    # Save the figure
    # os.makedirs(f'{cheminbase}/Figures/{NumExp}/{Type}_{Dossier}/', exist_ok=True)
    # plt.savefig(f'{cheminbase}/Figures/{NumExp}/{Type}_{Dossier}/_2d{j}.eps', format='eps', dpi=1000)

    z = np.ones((len(Pyc), NbProfil))
    for u in range(len(Pyc)):
        for m in range(1, NbProfil + 1, PasProfil):
            z[u, m] = m

    windowSize = 50
    a = 1
    b = (1 / windowSize) * np.ones(windowSize)

    ProfilDep = uniform_filter1d(ProfilDep, size=windowSize, axis=0)

    plt.figure()
    plt.plot3D(z[50:, ::PasProfil], hyP[50:], ProfilDep[50:, ::PasProfil], 'k')
    plt.plot3D(z[50:, profil1], hyP[50:], ProfilDep[50:, profil1], color='#77AC30', linewidth=4)
    plt.plot3D(z[50:, profil2], hyP[50:], ProfilDep[50:, profil2], color='#0072BD', linewidth=4)
    plt.plot3D(z[50:, profil3], hyP[50:], ProfilDep[50:, profil3], color='#A2142F', linewidth=4)

    plt.gca().invert_yaxis()

    plt.figure()
    plt.plot(hyP[50:], ProfilDep[50:, profil1], color='#77AC30', linewidth=2)
    plt.plot(hyP[50:], ProfilDep[50:, profil2], color='#0072BD', linewidth=2)
    plt.plot(hyP[50:], ProfilDep[50:, profil3], color='#A2142F', linewidth=2)
    plt.gca().invert_yaxis()

    # Save the figures
    # plt.savefig(f'{cheminbase}/Figures/{NumExp}/{Type}_{Dossier}/Profil2D_2d{j}.eps', format='eps', dpi=1000)

# Example usage
# Define variables with appropriate values
# plot_profil(AxisX, AxisY, Depl, LimMin, LimMax, Type, Unite, j, xmin_mm, xmax_mm, ymin_mm, ymax_mm, cheminbase, NumExp, NbProfil, PasProfil, profil1, profil2, profil3, Dossier)



def plot_save_correl_function(VisibilitePlot, Plot, LimMin, LimMax, Type, Unite, j, 
             xmin_mm, xmax_mm, ymin_mm, ymax_mm, NumExp, Folder_NameOut, path_base, 
             Quivers, Ux, Uy, AxisX, AxisY, scale):

    fig, ax = plt.subplots()

    if VisibilitePlot == 0:
        plt.ioff()  # Disable interactive mode to hide the plot

    
    

    im = ax.imshow(Plot, extent=(xmin_mm, xmax_mm, ymin_mm, ymax_mm), aspect='equal', cmap=cm.vik, origin = 'lower') #, vmin=LimMin, vmax=LimMax)
    #im = ax.imshow(Plot, aspect='auto', origin = 'lower', cmap=cm.vik) #, vmin=LimMin, vmax=LimMax)

    ax.set_xlabel('x [mm]')
    ax.set_ylabel('y [mm]')
    ax.tick_params(axis='both', labelsize=10)
    ax.set_aspect(aspect=1)  # This is an alternative to `axis equal`
    ax.invert_yaxis()

    cbar = plt.colorbar(im, ax=ax, orientation='vertical')
    cbar.set_label(f'{Type} {Unite}', fontsize=15)
    
    ax.annotate('', xy=(xmin_mm + 120, ymax_mm - 50), xytext=(xmin_mm + 30, ymax_mm - 50),
            arrowprops={"width":1.5,"headwidth":5,'headlength':5, 'color':'k'})

    if Quivers == 1:
        k = 303  # step size for the quivers
        Ux_Q = np.full(Ux.shape, np.nan)
        Uy_Q = np.full(Uy.shape, np.nan)
        for i in range(0, Ux.shape[0], k):
            for h in range(0, Ux.shape[1], k):
                if i + (k+1)//2 < Ux.shape[0] and h + (k+1)//2 < Ux.shape[1]:
                    Ux_Q[i+(k+1)//2, h+(k+1)//2] = Ux[i+(k+1)//2, h+(k+1)//2]
                    Uy_Q[i+(k+1)//2, h+(k+1)//2] = Uy[i+(k+1)//2, h+(k+1)//2]

        ax.quiver(AxisX, AxisY, Ux_Q, Uy_Q, scale=1, color='k')

    if scale == 'micrometre':
        displacement_text = f'total displacement = {j*0.025:.2f} mm'
    else:
        displacement_text = f'total displacement = {j*0.5:.2f} mm'
    ax.text(xmin_mm, ymin_mm - 10, displacement_text, color='k', fontsize=12)

    save_dir = os.path.join(path_base, 'Figures', NumExp, f'{Type}{Folder_NameOut}')
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.join(save_dir, f'{Type}-{j:.0f}.png')
    plt.savefig(filename, dpi=150, bbox_inches='tight')



# Example usage:
# plot_save_correl_function(VisibilitePlot, AxisXZ, AxisYZ, Plot, LimMin, LimMax, Type, Unite, j, xmin_mm, xmax_mm, ymin_mm, ymax_mm, onoff, Tdep, NumExp, Dep, Dossier, path_base, profil_mm, Quivers, Ux, Uy, AxisX, AxisY, SecondInv, Cmap, first_frame)