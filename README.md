# lpj_stuff

To get this running after building the executable ...

- You need to build the guess_utilities_1.3 and put a link to the bin directory in your path.

- On a mac, you need to setup gln (sudo ln -s gln ln) and greadlink (sudo ln -s greadlink readlink) as the mac versions don't replicate the linux ones. You can get these via the coreutils and I made symbolic links in /opt/local/bin

- ./benchmarks -s -i "pristine_sites" ../../../../runs/sites_test
