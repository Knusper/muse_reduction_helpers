#! /usr/bin/env bash

directory=$1
directory=`dirname ${directory}.`

# user specifies prefix of modded sky_continuum, e.g. `OIII_mod_Ha_mod_` for
# `OIII_mod_Ha_mod_SKY_CONTINUUM_0001.fits`
skycnt_prefix=$2

for soffile in $directory/*_basic_*/*_scipost_2.sof
do
    newsoffile=${soffile:0:-5}2_skycntmod.sof
    soffile_dir=${soffile:0:-4}
    cat $soffile > $newsoffile
    # remove original SKY_LINES entry from new .sof file
    sed -i '/SKY_LINES/d' $newsoffile
    # add SKY_LINES entry from second pass
    echo ${soffile_dir}/SKY_LINES_0001.fits  SKY_LINES >> $newsoffile
    # add modded sky_continuum
    echo ${soffile_dir}/${skycnt_prefix}SKY_CONTINUUM_0001.fits  SKY_CONTINUUM >> $newsoffile
done
