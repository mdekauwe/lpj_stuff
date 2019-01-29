#!/bin/bash

# Martin De Kauwe, 25th Jan 2018
MACHINE=$(uname -n | cut -c 1-4)
CLEAN=true

if [ $CLEAN == true ]; then
    rm -rf CMake* cmake_install.cmake cru framework guess_4.0.1 libraries
    rm -rf modules submit.sh

    cp zips/guess_4.0.1.tar.gz .
    gunzip < guess_4.0.1.tar.gz | tar -xvf -
    rm -rf guess_4.0.1.tar.gz
fi

if [ $MACHINE == "Mart" ] # my mac
then
    CMAKE_PREFIX_PATH=/opt/local/
elif [ $MACHINE == "raij" ] # nci
then
    module purge
    module load intel-cc/2019.0.117
    module load netcdf/4.3.3.1
    module load cmake/3.8.2
    module load intel-mpi/2019.0.117
    export CMAKE_PREFIX_PATH=$NETCDF_ROOT
    cmake guess_4.0.1
else                        # storm servers
    module purge
    #module load intel-cc/2019.0.117
    module load netcdf/4.1.3-intel
    module load cmake/2.8.11
    #module load intel-mpi/2019.0.117
    export CMAKE_PREFIX_PATH=$NETCDF_ROOT
    cmake guess_4.0.1
fi

# need to press "c" to configure and then "g" to generate the file
# it is worth doing a "t" to go into advanced mode to check it has set the
# netcdf libs correctly
ccmake guess_4.0.1

make
