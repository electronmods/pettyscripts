#!/bin/bash

shopt -s extglob

case "$1" in
    "-h" | "--help" )
        echo "Usage: random_password.sh [num_chars]"
        exit 0
        ;;
    +([0-9]) | "" )
        ;;
    *)
        echo "Must be integer argument"
        exit 1
        ;;
esac

tr -dc _A-Z-a-z-0-9 < /dev/urandom | head -c${1:-32} ; echo
