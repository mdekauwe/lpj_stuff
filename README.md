# lpj_stuff

To get this running after building the executable ...

- You need to build the guess_utilities_1.3 and put a link to the bin directory in your path (export PATH=$PATH:/Users/mdekauwe/research/lpj_guess_runs/utils/guess_utilities_1.3/bin
)

- On a mac, you need to setup gsplit (sudo ln -s gsplit split), gln (sudo ln -s gln ln) and greadlink (sudo ln -s greadlink readlink) as the mac versions don't replicate the linux ones. You can get these via the coreutils and I made symbolic links in /opt/local/bin

- cd lpj_guess_runs/src/guess_4.0.1/guess_4.0.1/benchmarks

- edit path.ins to match the path to the forcing files, e.g. param "file_co2"      (str "../../../../forcing/co2/co2_1901-2015_merged_NOAA_ESRL.txt". NB. I also uncommented the Location of EUROFLUX data and WATCH dirs


- ./benchmarks -s -i "pristine_sites" ../../../../runs/sites_test
