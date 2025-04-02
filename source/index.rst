.. **Superficial White Matter**
   ============================
.. title:: Supericial White Matter

.. raw:: html

   <style type="text/css">
      hr {
      width: 100%;
      height: 1px;
      background-color: #5D4BB7;
      margin-top: 24px;
      }
   </style>

**Welcome to SWM documentation!**
==========================================

.. Superficial White Matter documentation master file, created by
   sphinx-quickstart on 2024-04-02.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: ../figures/swm_logo.png
   :width: 20%
   :align: right

========================================
Superficial White Matter
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   examples
   references

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.11510179.svg
   :target: https://doi.org/10.5281/zenodo.11510179

.. image:: https://img.shields.io/github/issues/jordandekraker/superficial-white-matter
   :target: https://github.com/jordandekraker/superficial-white-matter/issues

.. image:: https://img.shields.io/github/stars/jordandekraker/superficial-white-matter.svg?style=flat&label=⭐%EF%B8%8F%20stars&color=brightgreen
   :target: https://github.com/jordandekraker/superficial-white-matter/stargazers

Citation
---------
> DeKraker, J., Cruces, R., & Hwang, Y. (2024). Superficial White Matter. Zenodo. https://doi.org/10.5281/zenodo.11510179

Description
------------
Superficial White Matter (SWM) generates surfaces at various white matter depths (default 1, 2, and 3 millimeters). The depths are calculated based on the real-world image resolution voxel size and transformed to millimeters.

Method
--------
This is done by first computing a Laplace field over white matter (cortex to subcortex+ventricles), and then shifting an existing white matter surface along that gradient. Stopping conditions are set by geodesic distance traveled.

.. image:: ../figures/swm_methods.png
   :alt: SWM Method

> White is the original WM surface, red, orange, and yellow are depths 1mm, 2mm, and 3mm accordingly.

Installation
------------

.. code-block:: bash

   git clone https://github.com/jordandekraker/superficial-white-matter.git
   pip install superficial-white-matter/

Usage with Freesurfer/Fastsurfer
--------------------------------

> The code expects *standard* NIFTI orientation, where the resolution is the diagonal of the header affine matrix. Running the inputs through `fslreorient2std` ensures that everything is calculated correctly.

.. code-block:: bash

   SUBJECTS_DIR=<path to surface subjects directory FreeSurfer/FastSurfer>
   SUBJECT=sub-01
   OUT=<path to output directory>
   aparc_aseg=${OUT}/${SUBJECT}_aparc+aseg.nii.gz
   mri_convert ${SUBJECTS_DIR}/${SUBJECT}/mri/aparc+aseg.mgz ${aparc_aseg}
   fslreorient2std ${aparc_aseg} ${aparc_aseg}

   # 1. Calculate the Laplace field
   python sWM/laplace_solver.py \
     ${aparc_aseg} \
     ${OUT}/${SUBJECT}_laplace-wm.nii.gz

   # 2. Generate the surfaces for each hemisphere
   for hemi in lh rh; do
     WM=${SUBJECTS_DIR}/${SUBJECT}/surf/${hemi}.white
     WM_gii=${OUT}/${SUBJECT}_hemi-${hemi}_label-white.surf.gii
     mris_convert ${WM} ${WM_gii}
     python sWM/surface_generator.py \
       "${WM_gii}" \
       ${OUT}/${SUBJECT}_laplace-wm.nii.gz \
       ${OUT}/${SUBJECT}_hemi-${hemi}_label-sWF_depth-
   done

More details on example usage can be found in [`example_usage.sh`](./example_usage.sh). SWM is implemented in [`micapipe v0.2.3`](https://github.com/MICA-MNI/micapipe/releases/tag/v0.2.3).

Modules
-------

**laplace_solver.py**

.. code-block:: python

   """
   Solves Laplace equation over the domain of white matter.
   Using grey matter as the source and ventricles as the sink.
   """

Usage:

.. code-block:: bash

   laplace_solver.py aparc+aseg.nii.gz laplace-wm.nii.gz

**surface_generator.py**

.. code-block:: python

   """
   Shifts a white matter surface inward along a Laplace field.
   """

Usage:

.. code-block:: bash

   surface_generator.py hemi-L_label-white.surf.gii laplace-wm.nii.gz



.. raw:: html

   <br>


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Getting started
   
   pages/installation
   pages/SWM_background

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Tutorials
   
   pages/tutorials_overview
   pages/tutorial_BigBrain
   pages/tutorial_AheadBrain
   pages/tutorial_MRI


__________________________________________________________________________________________________

.. raw:: html

   <br>
