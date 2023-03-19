#! /usr/bin/env bash

# run this after esorex_scibasic.sh has finished on an object
# > ./gen_sofs_for_scipost.sh ./obj_name/

object=$1

for dirname in ${object}/*basic*
do
    if [ -d ${dirname} ]; then
	echo $dirname
	python ./gen_sofs_for_scipost.py ${object} ${dirname}/
    fi
done
