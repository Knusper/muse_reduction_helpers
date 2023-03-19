#! /usr/bin/env python

# Run first, after downloading all the files from the ESO archive for one object.
# Download: raw data + processed calibrations !
# It is best to download the files into a folder that is named after the object,
# e.g. ./J0057-0941/
# Then run:
# `gen_sofs_for_scibasic.py ./J0057-0941/`
# replace ./J0057-0941/ with the object
# Next step: esorex_scibasic.sh

import sys,os
from glob import glob
from astropy.io import fits
from astropy.time import Time

# own function to generate the file lists based on the information
# provided in the fits header
from gen_file_list import gen_file_list

directory = sys.argv[1]
files = glob(directory + '*fits*')

# calibration frames
m_bias_list, m_bias_times = gen_file_list(files, 'HIERARCH ESO PRO CATG', 'MASTER_BIAS')
m_dark_list, m_dark_times = gen_file_list(files, 'HIERARCH ESO PRO CATG', 'MASTER_DARK')
m_flat_list, m_flat_times = gen_file_list(files, 'HIERARCH ESO PRO CATG', 'MASTER_FLAT')
tracet_list, tracet_times = gen_file_list(files, 'HIERARCH ESO PRO CATG', 'TRACE_TABLE')
wavect_list, wavect_times = gen_file_list(files, 'HIERARCH ESO PRO CATG', 'WAVECAL_TABLE')
geomet_list, geomet_times = gen_file_list(files, 'HIERARCH ESO PRO CATG', 'GEOMETRY_TABLE')
twilcb_list, twilcb_times = gen_file_list(files, 'HIERARCH ESO PRO CATG', 'TWILIGHT_CUBE')

# object frames & illum frames
object_list, object_times = gen_file_list(files, 'HIERARCH ESO DPR TYPE', 'OBJECT')
illumf_list, illumf_times = gen_file_list(files, 'HIERARCH ESO DPR TYPE', 'FLAT,LAMP,ILLUM')


for obj, obj_time in zip(object_list, object_times):

    obj_name = fits.getheader(obj)['OBJECT']
    sof_name = directory + obj_name + '_basic_' + os.path.basename(obj).removesuffix('fits.fz') + 'sof'
    sof_file = open(sof_name, 'w')

    sof_file.write(obj + '  OBJECT  \n')

    # find associated calibration which is closest in time and write to sof file
    illumf_min = (illumf_times - obj_time).argmin()
    m_bias_min = (m_bias_times - obj_time).argmin()
    m_dark_min = (m_dark_times - obj_time).argmin()
    m_flat_min = (m_flat_times - obj_time).argmin()
    tracet_min = (tracet_times - obj_time).argmin()
    wavect_min = (wavect_times - obj_time).argmin()
    geomet_min = (geomet_times - obj_time).argmin()
    twilcb_min = (twilcb_times - obj_time).argmin()

    sof_file.write(illumf_list[illumf_min] + '  ILLUM  \n')
    sof_file.write(m_bias_list[m_bias_min] + '  MASTER_BIAS  \n')
    sof_file.write(m_dark_list[m_dark_min] + '  MASTER_DARK \n')
    sof_file.write(m_flat_list[m_flat_min] + '  MASTER_FLAT \n')
    sof_file.write(tracet_list[tracet_min] + '  TRACE_TABLE \n')
    sof_file.write(wavect_list[wavect_min] + '  WAVECAL_TABLE \n')
    sof_file.write(geomet_list[geomet_min] + '  GEOMETRY_TABLE \n')
    sof_file.write(twilcb_list[twilcb_min] + '  TWILIGHT_CUBE \n')

    sof_file.close()
    print(sof_name + ' created...')
