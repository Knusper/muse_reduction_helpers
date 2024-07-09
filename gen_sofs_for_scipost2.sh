#! /usr/bin/env bash

directory=$1
directory=`dirname ${directory}.`

for soffile in $directory/*_basic_*/*_scipost_1.sof
do
    newsoffile=${soffile:0:-5}2.sof
    cat $soffile > $newsoffile
    echo ${directory}_reduced/OFFSET_LIST.fits  OFFSET_LIST >> $newsoffile
    echo ${directory}_reduced/DATACUBE_FINAL.fits  OUTPUT_WCS >> $newsoffile 
done
