#!/bin/bash
#
# submit.sh
#
# Portable bash script to run LPJ-GUESS version:
# BINARY
# as a parallel job using SLURM on Bristol's blue crystal.
#
# Created automatically on DATE
#
# Usage:
#
#   1. Copy script to the directory where you want output written.
#      This will be called the RUN DIRECTORY.
#   2. In an editor, set appropriate values for the variables NPROCESS,
#      INSFILE, GRIDLIST and OUTFILES (NB: no space after the = sign):

NPROCESS=28 # BC4 have two physical CPU chips (some would describe this as having two sockets), with 14 processing cores inside each; Slurm would say that this node has ‘28 CPUs’.
WALLTIME=00:10:00
MEMORY=16GB
INSFILE=global_cru.ins
INPUT_MODULE=cru_ncep
GRIDLIST="13_sites_gridlist_global_test.txt"
OUTFILES='*.out'
BINARY=guess

#      Where:
#      NPROCESS     = number of processes in parallel job
#      WALLTIME     = maximum wall (real) time for job hh:mm:ss
#      INSFILE      = path to ins file from run directory
#      INPUT_MODULE = input module to use
#      GRIDLIST     = path to gridlist file from run directory
#      OUTFILES     = list of LPJ-GUESS output files in single quotes,
#                     and separated by spaces (filenames only, including
#                     extension, no directory.) Shell wildcards are allowed.
#
#   3. Run the script using the command:
#        ./submit.sh
#      or:
#        ./submit.sh [-n <name>] [-s <file>] [-i <ins-file>]
#
#      All arguments are optional and interpreted as:
#      name     = the name of the job (shown in PBS queue)
#      file     = filename of a file which can override the variables
#                 above
#      ins-file = instruction file to use, overrides the INSFILE
#                 variable above
#
# Nothing to change past here
########################################################################

# Exit if any command fails
set -e

# Handle the command line arguments
while getopts ":n:s:i:" opt; do
    case $opt in
	n ) name=$OPTARG ;;
	s ) submit_vars_file=$OPTARG ;;
	i ) ins=$OPTARG ;;
    esac
done

# Override the submit variables with the contents of a file, if given
if [ -n "$submit_vars_file" ]; then
    source $submit_vars_file
fi

# Override INSFILE with the ins-file parameter, if given
if [ -n "$ins" ]; then
    INSFILE=$ins
fi

# On blue crystal, the recommendation is to submit jobs with the --exclusive
# option, so we get exclusive nodes. Since each node has 28 cores, we
# should set NPROCESS to a multiple of 28 to avoid waste.
# If you really want to, you could remove this check and the --exclusive
# option below, but your jobs might then be disturbed by other jobs
# sharing your nodes.
CORES_PER_NODE=28
if [[ $((NPROCESS%CORES_PER_NODE)) != 0 ]]; then
    echo "Please set NPROCESS to a multiple of 28 on Blue Crystal!" >&2
    exit 1
fi


# Convert INSFILE to an absolute path since we will be starting the
# guess instances from different directories.
# Please note when porting this script: readlink may not be available
# on non-Linux systems. Also, using absolute path names means the
# instruction file needs to be in a place accessible from the nodes.
INSFILE=$(readlink -f "$INSFILE")

GRIDLIST_FILENAME=$(basename $GRIDLIST)

# This function creates the gridlist files for each run by splitting
# the original gridlist file into approximately equal parts.
function split_gridlist {
    # Create empty gridlists first to make sure each run gets one
    for ((a=1; a <= NPROCESS ; a++))
    do
      echo > run$a/$GRIDLIST_FILENAME
    done

    # Figure out suitable number of lines per gridlist, get the number of
    # lines in original gridlist file, divide by NPROCESS and round up.
    local lines_per_run=$(wc -l $GRIDLIST | \
	awk '{ x = $1/'$NPROCESS'; d = (x == int(x)) ? x : int(x)+1; print d}')

    # Use the split command to split the files into temporary files
    split --suffix-length=4 --lines $lines_per_run $GRIDLIST tmpSPLITGRID_

    # Move the temporary files into the runX-directories
    local files=$(ls tmpSPLITGRID_*)
    local i=1
    for file in $files
    do
      mv $file run$i/$GRIDLIST_FILENAME
      i=$((i+1))
    done
}

# Create header of progress.sh script

echo "##############################################################" > progress.sh
echo "# PROGRESS.SH" >> progress.sh
echo "# Upload current guess.log files from local nodes and check" >> progress.sh
echo "# Usage: sh progress.sh" >> progress.sh
echo >> progress.sh

# Create a run subdirectory for each process and clean up

for ((a=1; a <= NPROCESS ; a++))
do
  mkdir -p run$a
  cd run$a ; rm -f guess.log ; rm -f $GRIDLIST_FILENAME ; cd ..
  echo "echo '********** Last few lines of ./run${a}/guess.log: **********'" >> progress.sh
  echo "tail ./run${a}/guess.log" >> progress.sh
done

split_gridlist



# Create SLURM script to request place in queue
cat <<EOF > guess.cmd
#!/bin/bash
#SBATCH -n $NPROCESS
#SBATCH --time=$WALLTIME
#SBATCH --exclusive
#SBATCH --mem=${MEMORY}

set -e

#module load languages/intel/2020-u4

module load libs/netcdf/4.7.3
module load libs/openmpi/4.1.1


#srun --mpi=pmi2 ${BINARY} -parallel -input $INPUT_MODULE $INSFILE
mpirun ${BINARY} -parallel -input $INPUT_MODULE $INSFILE

EOF

cat <<EOF > append.cmd
#!/bin/bash
#SBATCH -n 1
#SBATCH --time=$WALLTIME
set -e

function append_files {
    local number_of_jobs=\$1
    local file=\$2

    cp run1/\$file \$file

    local i=""
    for ((i=2; i <= number_of_jobs; i++))
    do
      if [ -f run\$i/\$file ]; then
        cat run\$i/\$file | awk 'NR!=1 || NF==0 || \$1 == \$1+0 { print \$0 }' >> \$file
      fi
    done
}

pushd run1 &> /dev/null
outfiles_unexpanded='$OUTFILES'
outfiles_expanded=\$(echo \$outfiles_unexpanded)
popd &> /dev/null

for file in \$outfiles_expanded
do
  append_files $NPROCESS \$file
done
cat run*/guess.log > guess.log
EOF

# Submit guess job
append_dependency=$(sbatch -J ${name:-"guess"} guess.cmd | awk '{print $NF}')

# Submit append job
sbatch --dependency=afterok:$append_dependency -J ${name:-"guess"}"_append" append.cmd
