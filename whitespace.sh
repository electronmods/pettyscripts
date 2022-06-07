#!/bin/bash

# from https://superuser.com/questions/763071/show-whitespace-characters-in-printout

sed 's/ /·/g;s/\t/￫/g;s/\r/§/g;s/$/¶/g'
