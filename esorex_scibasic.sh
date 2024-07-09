#! /usr/bin/env bash

directory=$1
extrarg=$2

for soffile in ${directory}/*_basic_MUSE*sof
do
    soffile_base=`basename ${soffile}`
    outdir=${directory}/${soffile_base%.sof}
    if [ ! -d "${outdir}" ]; then
	mkdir ${outdir}
    fi

    esorex --no-datamd5 --no-checksum --log-file=${outdir}/${soffile_base%.sof}.log \
	   --output-dir=${outdir} \
	   muse_scibasic --nifu=-1 --merge=true --resample=true \
	   ${extrarg} ${soffile}
done
