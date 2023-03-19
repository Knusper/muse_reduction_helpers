#! /usr/bin/env bash
# call: ./gen_sof_and_esorex_combine.sh ./obj_name/
# combined output then found in ./obj_name_reduced/

directory=$1

object=`basename ${directory}`
soffile=${object}_exp_combine.sof

if [ -e "${soffile}" ];then
    rm ${soffile}
fi

for file in ${directory}/*basic*/*scipost_1/PIXTABLE_REDUCED*
do
    echo ${file} PIXTABLE_REDUCED >> ${soffile}
done

echo ${object}_reduced/OFFSET_LIST.fits OFFSET_LIST >> ${soffile}

echo ${soffile} created...
echo -------
cat ${soffile}

read -p "Proceed (y/n)? " answer
case ${answer:0:1} in
    y|Y )

	esorex --no-checksum --no-datamd5 \
	       --log-file=${object}_exp_combine.log \
	       --output-dir=${object}_reduced \
	       muse_exp_combine ${soffile}
esac
