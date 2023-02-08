#!/bin/bash

# Thanks to https://superuser.com/a/561105

perl -pe 's/\x1b\[[0-9;]*[mG]//g'
