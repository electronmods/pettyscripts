#!/bin/bash

# squeak requires host name for postgres
export DB_HOST=broker.ro.db

# Output directory
outdir=/data/users/electron

# Capture script begin time for log filename
scriptbegin=$(date -Iseconds | sed -E 's/[-:]//g; s/T/_/; s/\+[0-9]{4}//')
echo "Session handle ${scriptbegin}"
echo "Use:"
echo "    grep wall *${scriptbegin}.log"
echo "to see the wall clock times of each run."
echo

# Define the test versions
# test_types=(lite pg pg.bk)
test_types=(pg pg)

                                # Iteration counts
i=1                             # We always start at 1
iopts=${#test_types[@]}         # Number of options (e.g. pg, lite, pg.bk...)
iruns=1                         # Number of times to run each option
imax=$(( $iruns * $iopts )) # Multiply number of runs by number of options

echo "Current PID $$" >&2

# Check to see if squeak is linked first, probably should do this a little more safely
if [ -h ./squeak ] ; then
    rm squeak
fi

while [ $i -le $imax ] ; do
	# Simple modulo chooser among the options
    sqver=${test_types[$(( ($i-1) % $iopts))]}

	# symlink the necessary folder to "squeak" to support hard-coded libraries
    ln -s squeak.${sqver} squeak
    cd squeak

    starttime=$(date --rfc-3339=seconds)
    echo "Try $i started, ${sqver}-style; time $starttime"

    echo $starttime >> ${outdir}/squeak.${sqver}.log
    { /usr/bin/time -v ./squeak.pl test.csv test_header.csv > ${outdir}/squeak.${sqver}.out ; } 2>> ${outdir}/squeak.${sqver}_${scriptbegin}.log
    # /usr/bin/time -v ./squeak.pl test.csv test_header.csv > ${outdir}/squeak.${sqver}.out

    endtime=$(date --rfc-3339=seconds)
    echo "Try $i ended; time $endtime"
    echo $endtime >> ${outdir}/squeak.${sqver}.log

    cd ..
    rm squeak
    i=$(( $i + 1 ))
done
