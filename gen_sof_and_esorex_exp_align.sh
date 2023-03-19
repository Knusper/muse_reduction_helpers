#! /usr/bin/env bash

directory=$1
extrarg=$2
# to use --threshold=-1 

object=`basename ${directory}`
soffile=${object}_exp_align.sof

if [ -e "${soffile}" ];then
    rm ${soffile}
fi

for file in ${directory}/*basic*/*scipost_1/IMAGE_FOV_0001.fits
do
    echo ${file} IMAGE_FOV >> ${soffile}
done

echo ${soffile} created...
echo -------
cat ${soffile}

read -p "Proceed (y/n)? " answer
case ${answer:0:1} in
    y|Y )
	if [ ! -d "${object}_reduced" ]; then
	    mkdir ${object}_reduced
	fi

	esorex --no-checksum --no-datamd5 \
	       --log-file=${object}_exp_align.log \
	       --output-dir=${object}_reduced \
	       muse_exp_align ${extrarg} ${soffile} 
    ;;
    * )
	echo You entered ${answer}...
    ;;
esac
