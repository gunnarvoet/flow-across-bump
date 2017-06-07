#!/usr/bin/env python
# coding: utf-8

# # BUMP
# Analyse results of barotropic flow over a bump mitgcm simulation

import scipy as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import xarray as xr
import cmocean

import warnings
warnings.filterwarnings('ignore')

DataDir = '/Volumes/svalbard/mitgcm/sp/BUMP/B5/run/allmnc/'
run = 'B5'

# ## Read model data
b6 = xr.open_dataset(DataDir+'diag1.glob.nc')
b6s = xr.open_dataset(DataDir+'state.glob.nc')
grid = xr.open_dataset(DataDir+'grid.glob.nc')

# center of domain in km
my = grid.Y.mean()/1000
print(my)

deltay = 10
yi = np.where((grid.Y/1000>my-deltay) & (grid.Y/1000<my+deltay))
yp1i = np.where((grid.Yp1/1000>my-deltay) & (grid.Yp1/1000<my+deltay))
w = b6.WVEL.isel(Y=yi[0])
v = b6.VVEL.isel(Yp1=yp1i[0])
eps = b6.KLeps.isel(Y=yi[0])
th = b6.THETA.isel(Y=yi[0])


for ti, tt in enumerate(b6['T'].values):
	
	timestr = 'T = {:2.1f} hrs'.format(tt/3600)
	print(timestr)
	
	fig, ax = plt.subplots(ncols=3, nrows=1, figsize=(14,4), sharex=True, sharey=True)

	# v
	h = ax[0].pcolormesh(v.Yp1.values/1000, grid.Z.values, np.squeeze(v.isel(T=ti).values), cmap='RdBu_r', vmin=-0.7, vmax=0.7)
	ax[0].contour(th.Y.values/1000, grid.Z.values, np.squeeze(th.isel(T=ti).values),
	            levels=np.arange(1.6,3,0.1), colors='k', alpha=0.2, linewdiths=5)
	ax[0].plot(grid.Y.isel(Y=yi[0])/1000, -grid.Depth.isel(Y=yi[0]), color='0.1', linewidth=0.5)
	plt.colorbar(h, extend='both', ax=ax[0], label='v [m/s]')
	
	ax[0].annotate(timestr, xy=(0.05,0.95), xycoords='axes fraction')
	ax[0].set(ylabel='z [m]', xlabel='y [km]', xlim=(my-deltay, my+deltay))

	# w
	h = ax[1].pcolormesh(w.Y.values/1000, grid.Z.values, np.squeeze(w.isel(T=ti).values), cmap='RdBu_r', vmin=-0.2, vmax=0.2)
	ax[1].contour(th.Y.values/1000, grid.Z.values, np.squeeze(th.isel(T=ti).values),
	            levels=np.arange(1.6,3,0.1), colors='k', alpha=0.2, linewdiths=5)
	ax[1].plot(grid.Y.isel(Y=yi[0])/1000, -grid.Depth.isel(Y=yi[0]), color='0.1', linewidth=0.5)
	plt.colorbar(h, extend='both', ax=ax[1], label='w [m/s]')

	# epsilon
	tmp = np.squeeze(eps.isel(T=ti).values)
	tmp2 = np.ma.masked_less(tmp,1e-12,copy=True)
	h = ax[2].pcolormesh(eps.Y.values/1000, grid.Z.values, np.log10(tmp2), cmap='Spectral_r', vmin=-12, vmax=-5)
	ax[2].contour(th.Y.values/1000, grid.Z.values, np.squeeze(th.isel(T=ti).values),
	            levels=np.arange(1.6,3,0.1), colors='k', alpha=0.2, linewdiths=5)
	ax[2].plot(grid.Y.isel(Y=yi[0])/1000, -grid.Depth.isel(Y=yi[0]), color='0.1', linewidth=0.5)
	plt.colorbar(h, extend='both', ax=ax[2], label='log$_{10}$($\epsilon$) [W/kg]')

	plt.tight_layout()
	PrintName = 'movie_{:s}/frame{:04d}.png'.format(run, ti)
	plt.savefig(PrintName, dpi=200)