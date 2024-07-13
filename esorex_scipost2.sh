#! /usr/bin/env bash
# Usage: esorex_scipost2.sh ./OBJ_DIR/
# (make sure to wrap ./OBJ_DIR/ accordingly

directory=$1
extrarg=$2

# run esorex
for soffile in $directory/*_basic_*/*_scipost_2.sof
do
    outdir=${soffile%.sof}
    if [ ! -d "${outdir}" ]; then
	mkdir ${outdir}
    fi
    logname=`basename ${soffile}`

    esorex --no-datamd5 --no-checksum --log-file=${outdir}/${logname%sof}log \
	   --output-dir=${outdir}/ \
	   muse_scipost --save=cube,individual,skymodel --autocalib=deepfield ${extrarg} ${soffile}

done

echo "linking output files"
for cubefile in ${directory}/*basic*/*scipost_2/DATACUBE_FINAL.fits
do
    outfile=`echo $cubefile | rev | sed 's\/\_\' | rev`
    outfile=`basename $outfile`
    echo ln -v ${cubefile}  $(basename $directory)_reduced/${outfile}
done
