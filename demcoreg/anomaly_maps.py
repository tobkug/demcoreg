#! /usr/bin/env python

"""
Create anomaly map time series
"""

import os
import sys
import glob

import numpy as np
import matplotlib.pyplot as plt

from pygeotools.lib import iolib, timelib, malib
from imview.lib import pltlib

outdir = 'stack_anomaly'
if not os.path.exists(outdir):
    os.makedirs(outdir)

#dem_fn_list = glob.glob('*8m_trans_warp.tif')
#stack = malib.DEMStack(dem_fn_list, med=True)
#dem_ref_fn = 'rainier_allgood_mos-tile-0_warp.tif'
#dem_ref = iolib.fn_getma(dem_ref_fn)

stack_fn = sys.argv[1]
stack = malib.DEMStack(stack_fn=stack_fn, med=True)
dem_fn_list = stack.fn_list 
dem_ref = stack.stack_med
anomaly_stack = stack.ma_stack - dem_ref
anomaly_clim = np.max(np.abs(malib.calcperc(anomaly_stack, (2,98))))
anomaly_clim = (-anomaly_clim, anomaly_clim)

#for dem_fn in [dem_ref_fn]+dem_fn_list:
for n, dem_fn in enumerate(dem_fn_list):
    print('%i of %i: %s' % (n+1, len(dem_fn_list), dem_fn))
    #print(dem_fn)
    #dem_ds = iolib.fn_getds(dem_fn)
    #dem = iolib.ds_getma(dem_ds)
    dem_fn = stack.fn_list[n]
    title = dem_fn
    dem = stack.ma_stack[n]
    anomaly = anomaly_stack[n]
    #dem_clim = malib.calcperc(stack.ma_stack, (2,98))
    #dem_hs_fn = os.path.splitext(dem_fn)[0]+'_hs_az315.tif'
    #dem_hs = iolib.fn_getma(dem_hs_fn)
    #dt = timelib.fn_getdatetime(dem_fn)
    dt = stack.date_list[n]
    #if dt is not None:
        #title = dt.strftime('%Y-%m-%d')
    #f = makefig(dem, dem_hs, anomaly, ds=dem_ds, title=title)
    f,ax = plt.subplots()
    im = ax.imshow(anomaly, clim=anomaly_clim, cmap='RdBu')
    pltlib.add_cbar(ax, im)
    pltlib.hide_ticks(ax)
    ax.set_facecolor('k')
    if title is not None:
        ax.set_title(title)
    out_fn = os.path.join(outdir, os.path.splitext(os.path.split(dem_fn)[-1])[0]+'_anomaly.png')
    f.savefig(out_fn, bbox_inches='tight', dpi=150)

def makefig(dem, hs, anomaly, ds, title=None):
    f,axa = plt.subplots(1, figsize=(8,5))
    dem_clim = (1600, 2100)
    
    hs_clim = (1, 255)
    anomaly_clim = (-15, 15)
    hs_im = axa[0].imshow(hs, vmin=hs_clim[0], vmax=hs_clim[1], cmap='gray')
    dem_im = axa[0].imshow(dem, vmin=dem_clim[0], vmax=dem_clim[1], cmap='cpt_rainbow', alpha=0.5)
    res = 8
    pltlib.add_scalebar(axa[0], res=res)
    pltlib.add_cbar(axa[0], dem_im, label='Elevation (m WGS84)')
    anomaly_im = axa[1].imshow(anomaly, vmin=anomaly_clim[0], vmax=anomaly_clim[1], cmap='RdBu')
    pltlib.add_cbar(axa[1], anomaly_im, label='Elevation Anomaly (m)')
    plt.tight_layout()
