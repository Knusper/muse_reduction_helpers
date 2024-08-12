#! /usr/bin/env bash

directory=$1
directory=`dirname ${directory}.`

for soffile in $directory/*_basic_*/*_scipost_2.sof
do
    newsoffile=${soffile:0:-5}3.sof
    cat $soffile > $newsoffile
    echo ${directory}_reduced/mask_cont_im_DATACUBE_scipost_2_mpdaf_cmbd.fits  SKY_MASK >> $newsoffile
done
