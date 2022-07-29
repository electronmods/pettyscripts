#!/bin/bash

for e in `cat ~/working_list.txt` ; do
( cd $e && git diff --name-status | \
    wc -l | \
    ( read n && \
    if [[ $n > 0 ]] ; then
        echo $e
    fi
    )
)
done
