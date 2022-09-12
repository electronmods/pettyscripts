#!/bin/bash

# qfind.sh - Quietly find files without all the stderr permissions noise

set -f

if [[ "$1" == "" ]] ; then
    >&2 echo "Usage: $(basename $0) <dir> <pattern> [extra args]"
    exit 1
fi

if [[ "$2" == "" ]] ; then
    findpat='*'
fi

finddir="$1"
findpat="${findpat:-$2}"
shift 2

if [[ ! -d "$finddir" ]] ; then
    >&2 echo "Directory '$finddir' invalid."
    exit 1
fi

echo "find \"$finddir\" -iname \"$findpat\" $@ 2>/dev/null"
find "$finddir" -iname "$findpat" $@ 2>/dev/null

