#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import os

os.system('less STDOUT.000* | grep CFL_w > tmp.txt')
os.system('cut -c10-13 -c58- tmp.txt > tmp3.txt')
tmp = np.loadtxt('tmp3.txt')
os.system('rm tmp.txt tmp3.txt')
ii = tmp[:,0]
cflw = np.reshape(tmp[:,1],(8,-1))
cflw = cflw.T

os.system('less STDOUT.000* | grep CFL_v > tmp.txt')
os.system('cut -c10-13 -c58- tmp.txt > tmp3.txt')
tmp = np.loadtxt('tmp3.txt')
os.system('rm tmp.txt tmp3.txt')
ii2 = tmp[:,0]
cflv = np.reshape(tmp[:,1],(8,-1))
cflv = cflv.T

fig, ax = plt.subplots(nrows=2, ncols=1, sharey=True, sharex=True)
ax[0].plot(cflw)
ax[0].set_ylabel('CFL w')
ax[1].plot(cflv)
ax[1].set_ylabel('CFL v')
[axi.grid('on') for axi in ax]
plt.savefig('cfl.png')

os.system('open cfl.png')