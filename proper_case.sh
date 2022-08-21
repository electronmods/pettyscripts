#!/bin/bash

# From https://unix.stackexchange.com/questions/554901/how-to-change-any-text-to-proper-case-and-sentence-case-using-tr
# which also has some sentence case stuff.

sed -E "s/[[:alnum:]_'-]+/\u&/g"
