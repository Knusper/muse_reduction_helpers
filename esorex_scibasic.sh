#! /usr/bin/env bash

# Run after all the sof files for muse_scibasic have been created with
# gen_sofs_for_scibasic.py
# Run: `esorex_scibasic.sh ./J0057-0941/` (replace J0057-0941 with the name of the object)

directory=$1
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
	   ${soffile}
done
