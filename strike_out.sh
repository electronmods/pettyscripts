#!/bin/bash

# Useful for clearing out passwords or credentials on the command line
# Receives only one argument, which is one character to strike out the
# input from stdin.

# Defaults to "*" if no argument given.

if [[ ${#1} -gt 1 ]] ; then
    >&2 echo "One argument, one character only. Got \"$1\"."
    exit 1
elif [[ ${#1} -eq 0 ]] ; then
    ch="*"
else
    ch="$1"
fi

sed -e "s/./$ch/g"
