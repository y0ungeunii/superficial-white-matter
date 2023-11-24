# code from https://github.com/khanlab/hippunfold/blob/master/hippunfold/workflow/scripts/create_warps.py

# shifts a wm surface inward along a Laplace field

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
    depth = arg2float_list(sys.argv[4])
else:
    depth = [1,2,3] # default depths

convergence_threshold = 1e-4
step_size = 0.1 # vox
max_iters = int(np.max(np.diff(depth))/step_size)*10


# load data
surf = nib.load(in_surf)
V = surf.get_arrays_from_intent('NIFTI_INTENT_POINTSET')[0].data
F = surf.get_arrays_from_intent('NIFTI_INTENT_TRIANGLE')[0].data
laplace = nib.load(in_laplace)
lp = laplace.get_fdata()
print('loaded data and parameters')

# laplace to gradient
dx,dy,dz = np.gradient(lp)

distance_travelled = np.zeros((len(V)))
n=0
for d in depth:
    # apply inverse affine to surface to get to matrix space
    print(laplace.affine)
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

    nib.save(surf, out_surf_prefix + str(d) + 'vox.surf.gii')
