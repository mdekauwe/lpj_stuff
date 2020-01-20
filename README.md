# lpj_stuff

To get this running after building the executable ...

- You need to build the guess_utilities_1.3 and put a link to the bin directory in your path (export PATH=$PATH:/Users/mdekauwe/research/lpj_guess_runs/utils/guess_utilities_1.3/bin
)

- On a mac, you need to setup gsplit (sudo ln -s gsplit split), gln (sudo ln -s gln ln) and greadlink (sudo ln -s greadlink readlink) as the mac versions don't replicate the linux ones. You can get these via the coreutils and I made symbolic links in /opt/local/bin

    cd lpj_guess_runs/src/guess_4.0.1/guess_4.0.1/benchmarks

- edit path.ins to match the path to the forcing files, e.g. param "file_co2"      (str "../../../../forcing/co2/co2_1901-2015_merged_NOAA_ESRL.txt". NB. I also uncommented the Location of EUROFLUX data and WATCH dirs


    ./benchmarks -s -i "pristine_sites" ../../../../runs/sites_test


## GADI stuff

NETCDF_CXX_LIBRARY is not found on gadi, I think this is because in /apps/netcdf/4.7.1/lib, there is a 4 in libnetcdf_c++4.so@. So, in the build script you need to explictly set this lib yourself as I think the 4 is throwing things off.

There is a further issue with the PJ_ob_tran.c file:

    $ cd utils/guess_utilities_1.3/gmap/libproj4/misc/
    $ vi PJ_ob_tran.c

change line 45

    // change by mgdk to compile, 20/01/2020
    if (xy.x != HUGE_VAL && P->rot) {
    //if (xy.x != HUGE && P->rot) {
