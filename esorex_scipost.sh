#! /usr/bin/env bash

directory=$1

for soffile in $directory/*_basic_*/*_scipost_1.sof
do
    outdir=${soffile%.sof}
    if [ ! -d "${outdir}" ]; then
	mkdir ${outdir}
    fi
    logname=`basename ${soffile}`

    esorex --no-datamd5 --no-checksum --log-file=${outdir}/${logname%sof}log \
	   --output-dir=${outdir}/ \
	   muse_scipost --save=cube,individual,skymodel ${soffile}

done
