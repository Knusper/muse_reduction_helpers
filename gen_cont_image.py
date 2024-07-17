#! /usr/bin/env python

import argparse
import os
import sys
from os.path import basename, dirname
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np

# from lsd_cat_library
from line_em_funcs import hierarch_multi_line, wavel

# store command that was entered by the user
command = os.path.basename(sys.argv[0])
for entity in sys.argv[1:]:
    command = command + " " + entity

parser = argparse.ArgumentParser(
    description="""
Generate continuum image given a set of wavelength regions.
"""
)
parser.add_argument(
    "-i",
    "--input",
    required=True,
    type=str,
    help="""Name of the input FITS file containing the flux and variance
datacube.""",
)
parser.add_argument(
    "-l",
    "--layers",
    required=True,
    nargs="*",
    help="""List of layer
boundaries for included regions: ---layers start_1 end_1 start_2 end_2 .... """,
)
args = parser.parse_args()

cube_filename = args.input
layers = args.layers

cont_regs = [(int(layers[i]), int(layers[i + 1])) for i in range(0, len(layers), 2)]

cube_basename = basename(cube_filename)
cube_pathname = dirname(cube_filename)
out_name_base = cube_pathname + cube_basename.split(".")[:-1][0]

############

hdu = fits.open(cube_filename)
data = hdu["DATA"].data  #
vari = hdu["STAT"].data
header = hdu["DATA"].header

# MODIFY FITS HEADER FOR OUTPUT IMAGE
# The following simple thing does not work - as it creates PCi_j transformation elements
# but muse_pipeline requires CDi_j elements
# wcs = WCS(header)
# ima_wcs = wcs.sub(2)
# ima_wcs_head = ima_wcs.to_header()
# ... so we have to do this instead
ima_wcs_head = header.copy()
ima_wcs_head['WCSAXES'] = 2
ima_wcs_head['NAXIS'] = 2
for key in ['NAXIS3', 'CRVAL3', 'CRPIX3', 'CUNIT3', 'CTYPE3', 'CD3_3', 'CD1_3',
            'CD3_1', 'CD3_2']:
    ima_wcs_head.remove(key)

ima_wcs_head = hierarch_multi_line(
    ima_wcs_head,
    "HIERARCH CONT LAYERS",
    " ".join(layers),
    "",
)
ima_wcs_head = hierarch_multi_line(
    ima_wcs_head, "HIERARCH CONT INPUT", cube_filename, ""
)

im = np.zeros_like(data[0])
var_im = im.copy()

xax = wavel(header)

print("Summing over spectral layers ...")
print("z_min z_max lambda_min lambda_max")
for cont_reg in cont_regs:
    print(
        str(cont_reg[0]).rjust(5)
        + " "
        + str(cont_reg[1]).rjust(5)
        + " "
        + str(round(xax[cont_reg[0]], 2)).rjust(10)
        + " "
        + str(round(xax[cont_reg[1]], 2)).rjust(10)
    )
    im += np.sum(data[cont_reg[0] : cont_reg[1] + 1, :, :], axis=0)
    var_im += np.sum(vari[cont_reg[0] : cont_reg[1] + 1, :, :], axis=0)

# erg/s/cm^2/Angstrom -> erg/s/cm^2
im *= header["CD3_3"]
var_im *= header["CD3_3"] ** 2

ima_wcs_head["BUNIT"] = "10**(-20) erg/s/cm**2"
ima_wcs_head["HISTORY"] = "--- start of gen_cont_image.py command ---"
ima_wcs_head["HISTORY"] = command
ima_wcs_head["HISTORY"] = "--- end of gen_cont_image.py command ---"

if cube_pathname == "":
    cube_pathname = "./"

cont_image_name = cube_pathname + "/cont_im_" + cube_basename
fits.writeto(cont_image_name, im, header=ima_wcs_head)
print("Continuum image saved to: " + cont_image_name)
noise_image_name = cube_pathname + "/noise_im_" + cube_basename
fits.writeto(noise_image_name, np.sqrt(var_im), header=ima_wcs_head)
print("Noise image saved to: " + noise_image_name)
