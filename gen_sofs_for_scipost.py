#! /usr/bin/env python

# USAGE EXAMPLE:
#-----------------------------------------------------------------#
#  for dirname in ./J0519+0007/*_basic_*                          #
#   do                                                            #
#    if [ -d ${dirname} ]; then                                   #
#     echo $dirname                                               #
#     python ./gen_sofs_for_scipost.py ./J0519+0007/ $dirname/    #
#    fi                                                           #
#   done                                                          #
#-----------------------------------------------------------------#
# ...
# but normally `gen_sofs_for_scipost.sh ./J0519+0007/` should take care of it
# ...

import sys, os
from glob import glob
from astropy.io import fits
from astropy.time import Time

from gen_file_list import gen_file_list

download_directory = sys.argv[1]
scibasic_directory = sys.argv[2]

dldir_files = glob(download_directory + "*fits*")
pxtbl_files = sorted(glob(scibasic_directory + "PIXTABLE*fits"))

obj_time = Time(fits.getheader(pxtbl_files[0], 0)["DATE-OBS"], format="fits")
obj_name = fits.getheader(pxtbl_files[0], 0)["OBJECT"]

stdrsp_list, stdrsp_times = gen_file_list(
    dldir_files, "HIERARCH ESO PRO CATG", "STD_RESPONSE"
)
stdtlr_list, stdtlr_times = gen_file_list(
    dldir_files, "HIERARCH ESO PRO CATG", "STD_TELLURIC"
)
lsprof_list, lsprof_times = gen_file_list(
    dldir_files, "HIERARCH ESO PRO CATG", "LSF_PROFILE"
)
astrmt_list, astrmt_times = gen_file_list(
    dldir_files, "HIERARCH ESO PRO CATG", "ASTROMETRY_WCS"
)

# there should be only one of each for the next categories - thats why
# we have [0] at the end
sky_line_file = gen_file_list(
    dldir_files, "HIERARCH ESO PRO CATG", "SKY_LINES", times=False
)[0]
flt_list_file = gen_file_list(
    dldir_files, "HIERARCH ESO PRO CATG", "FILTER_LIST", times=False
)[0]
ext_tabl_file = gen_file_list(
    dldir_files, "HIERARCH ESO PRO CATG", "EXTINCT_TABLE", times=False
)[0]

# sof file out
timestamp = scibasic_directory[scibasic_directory.rfind("basic") + 6 : -1]
sof_name = (
    scibasic_directory
    + "/"
    + obj_name.replace(" ", "_")
    + "_"
    + timestamp
    + "_scipost_1.sof"
)
sof_file = open(sof_name, "w")

for filename in pxtbl_files:
    sof_file.write(filename + "  PIXTABLE_OBJECT \n")

# finding the calibration frames closest in time
sof_file.write(stdrsp_list[(stdrsp_times - obj_time).argmin()] + "  STD_RESPONSE \n")
sof_file.write(stdtlr_list[(stdtlr_times - obj_time).argmin()] + "  STD_TELLURIC \n")
sof_file.write(lsprof_list[(lsprof_times - obj_time).argmin()] + "  LSF_PROFILE \n")
sof_file.write(astrmt_list[(astrmt_times - obj_time).argmin()] + "  ASTROMETRY_WCS \n")

sof_file.write(sky_line_file + "  SKY_LINES \n")
sof_file.write(flt_list_file + "  FILTER_LIST \n")
sof_file.write(ext_tabl_file + "  EXTINCT_TABLE \n")
sof_file.close()

print(sof_name + " created...")
