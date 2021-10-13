#!/bin/bash

# Martin De Kauwe, 13th Oct 2021
MACHINE=$(uname -n | cut -c 1-4)
CLEAN=true

if [ $CLEAN == true ]; then
    rm -rf CMakeCache.txt CMakeFiles Makefile cmake_install.cmake
    rm -rf cru framework guess_4.1 libraries modules

    cp ../zips/guess_4.1.tar.gz .
    gunzip < guess_4.1.tar.gz | tar -xvf -
    rm -rf guess_4.1.tar.gz
fi

if [ $MACHINE == "Mart" ] # my mac
then
    CMAKE_PREFIX_PATH=/opt/local/
    cmake guess_4.1
elif [ $MACHINE == "FVFG" ] # bristol mac
then
    CMAKE_PREFIX_PATH=/opt/local/
    cmake guess_4.1
elif [ $MACHINE == "gadi" ] # nci
then
    module purge
    module load pbs
    module load dot
    module load cdo/1.9.8
    module load intel-compiler/2019.3.199
    module load intel-mpi/2019.6.166
    module load netcdf/4.7.1
    export CMAKE_PREFIX_PATH=$NETCDF_ROOT
    cmake guess_4.0.1
else                        # storm servers
    module purge
    #module load intel-cc/2019.0.117
    module load netcdf/4.1.3-intel
    module load cmake/2.8.11
    export CMAKE_PREFIX_PATH=$NETCDF_ROOT
    cmake guess_4.0.1
fi

# need to press "c" to configure and then "g" to generate the file
# it is worth doing a "t" to go into advanced mode to check it has set the
# netcdf libs correctly
#ccmake guess_4.0.1

make
