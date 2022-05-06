#!/bin/bash

# Martin De Kauwe, 25th Jan 2018
MACHINE=$(uname -n | cut -c 1-4)
CLEAN=true

if [ $CLEAN == true ]; then
    rm -rf CMake* cmake_install.cmake cru framework guess_4.0.1 libraries
    rm -rf modules submit.sh

    #cp zips/guess_4.0.1.tar.gz .
    cp zips/guess_4.0.1_post2020_ndep_patch.tar.gz .
    #gunzip < guess_4.0.1.tar.gz | tar -xvf -
    gunzip < guess_4.0.1_post2020_ndep_patch.tar.gz | tar -xvf -
    #rm -rf guess_4.0.1.tar.gz
    rm -rf guess_4.0.1_post2020_ndep_patch.tar.gz
fi

if [ $MACHINE == "Mart" ] # my mac
then
    CMAKE_PREFIX_PATH=/opt/local/
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
elif [ $MACHINE == "bc4l" ] # Bristol
then
    #module load languages/intel/2020-u4

    module load tools/cmake/3.20.0
    module load libs/netcdf/4.7.3
    module load libs/openmpi/4.1.1

    module load CMake/3.9.5-GCCcore-6.4.0
    export CMAKE_PREFIX_PATH=/mnt/storage/software/libraries/gnu/netcdf-4.7.3
    cmake guess_4.0.1
else
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
