# remove old netcdf files in this directory
rm *.nc

# link all files
ln -s ../mnc_*/grid*.nc .
ln -s ../mnc_*/state*.nc .
ln -s ../mnc_*/diag1*.nc .
ln -s ../mnc_*/diag2*.nc .
ln -s ../mnc_*/phiHyd*.nc .

# activate python 2.7 for gluemncbig
# need to install this using
#   conda create -n py27 python=2.7
# if missing
source activate py27

# glue all files
gluemncbig -o grid.glob.nc grid.t00*.nc
gluemncbig -o state.glob.nc state.*.t00*.nc
gluemncbig -o diag1.glob.nc diag1.*.t00*.nc
gluemncbig -o diag2.glob.nc diag2.*.t00*.nc
gluemncbig -o phiHyd.glob.nc phiHyd.*.t00*.nc

# deactivate python 2.7
source deactivate py27