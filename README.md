# lpj_stuff

To get this running after building the executable ...

- You need to build the guess_utilities_1.3 and put a link to the bin directory in your path (export PATH=$PATH:/Users/mdekauwe/research/lpj_guess_runs/utils/guess_utilities_1.3/bin
)

- On a mac, you need to setup gln (sudo ln -s gln ln) and greadlink (sudo ln -s greadlink readlink) as the mac versions don't replicate the linux ones. You can get these via the coreutils and I made symbolic links in /opt/local/bin

- cd lpj_guess_runs/src/guess_4.0.1/guess_4.0.1/benchmarks
- ./benchmarks -s -i "pristine_sites" ../../../../runs/sites_test
