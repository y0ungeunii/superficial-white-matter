#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shifts a white matter surface inward along a Laplace field

Parameters
----------
GIFTI  :    str
            White matter surface in GIFTI format (surf.gii)
NIFTI  :    str
            laplacian image generated by laplace_solver.py
OUTPUT :    str
            path and name to the output surfaces
DEPTHS :    list [int | float] (OPTIONAL)
            DEFAULT=[1,2,3] List of depths to sample (in voxels)

Returns
-------
NIFTI
    a list of strings representing the header columns

Usage
-----
surface_generator.py hemi-L_label-white.surf.gii laplace-wm.nii.gz hemi-L_label-sWF_depth-

Created on October 2023

@author: Jordan DeKraker
code from https://github.com/khanlab/hippunfold/blob/master/hippunfold/workflow/scripts/create_warps.py

"""

import copy
import nibabel as nib
import numpy as np
from scipy.interpolate import RegularGridInterpolator
import sys

print('starting surface shift')

# here we will set some parameters
in_surf = sys.argv[1]
in_laplace = sys.argv[2]
out_surf_prefix = sys.argv[3]
def arg2float_list(arg):
    return list(map(float, arg.split(',')))
if len(sys.argv)>4:
    depth_mm = arg2float_list(sys.argv[4])
else:
    depth_mm = [1,2,3] # default depths in mm

# load data
surf = nib.load(in_surf)
V = surf.get_arrays_from_intent('NIFTI_INTENT_POINTSET')[0].data
F = surf.get_arrays_from_intent('NIFTI_INTENT_TRIANGLE')[0].data
laplace = nib.load(in_laplace)
lp = laplace.get_fdata()
print('loaded data and parameters')

# Get image resolution
# print(laplace.affine)
xres = laplace.affine[0, 0]
yres = laplace.affine[1, 1]
zres = laplace.affine[2, 2]

# Convert depths from mm to voxels
depth_vox = [round(depth / xres, 3) for depth in depth_mm]

# Convert depth values to strings with a specific format
depth_str = [f'{d:.1f}' for d in depth_mm]  # Use one decimal places

convergence_threshold = 1e-4
step_size = 0.1 # vox
max_iters = int(np.max(np.diff(depth_mm))/step_size)*10

# laplace to gradient
dx,dy,dz = np.gradient(lp)

# Scale the gradients by the image resolutions to handle anisotropy
dx = dx / xres
dy = dy / yres
dz = dz / zres

distance_travelled = np.zeros((len(V)))
n=0
for d, d_str in zip(depth_vox, depth_str):
    # apply inverse affine to surface to get to matrix space
    V[:,:] = V - laplace.affine[:3,3].T
    for xyz in range(3):
        V[:,xyz] = V[:,xyz]*(1/laplace.affine[xyz,xyz])
    for i in range(max_iters):
        Vnew = copy.deepcopy(V)
        pts = distance_travelled < d
        V_tmp = Vnew[pts,:].astype(int)
        stepx = dx[V_tmp[:,0],V_tmp[:,1],V_tmp[:,2]]
        stepy = dy[V_tmp[:,0],V_tmp[:,1],V_tmp[:,2]]
        stepz = dz[V_tmp[:,0],V_tmp[:,1],V_tmp[:,2]]
        magnitude = np.sqrt(stepx**2 + stepy**2 + stepz**2)
        for m in range(len(magnitude)):
            if magnitude[m]>0:
                stepx[m] = stepx[m] * (step_size/magnitude[m])
                stepy[m] = stepy[m] * (step_size/magnitude[m])
                stepz[m] = stepz[m] * (step_size/magnitude[m])
        Vnew[pts,0] += stepx
        Vnew[pts,1] += stepy
        Vnew[pts,2] += stepz
        distance_travelled[pts] += step_size
        ssd = np.sum((V-Vnew)**2,axis=None)
        print(f'itaration {i}, convergence: {ssd}, still moving: {np.sum(pts)}')
        if ssd < convergence_threshold:
            break
        V[:,:] = Vnew[:,:]
    # return to world coords
    for xyz in range(3):
        V[:,xyz] = V[:,xyz]*(laplace.affine[xyz,xyz])
    V[:,:] = V + laplace.affine[:3,3].T

    nib.save(surf, out_surf_prefix + d_str + 'mm.surf.gii')
