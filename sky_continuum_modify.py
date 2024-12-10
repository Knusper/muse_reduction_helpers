#! /usr/bin/env python

import argparse
from astropy.table import Table
from astropy.io import fits
from matplotlib import pyplot as plt
import numpy as np
import os, sys

# get string of the commandline that entered by the user
command = os.path.basename(sys.argv[0])
for entity in sys.argv[1:]:
    command = command + " " + entity

### ARGUMENT PARSING ###
parser = argparse.ArgumentParser(
    description="""sky_continuum_modify.py

Linearly interpolate from lambda1 to lambda2 in supplied SKY_CONTINUUM file from MUSE DRS.
"""
)
parser.add_argument(
    "-i",
    "--input",
    type=str,
    required=True,
    help="Name of the input SKY_CONTINUUM fits file.",
)
parser.add_argument(
    "-o", "--output", type=str, required=True, help="Name of the output fits file."
)
parser.add_argument(
    "--lambda1",
    type=float,
    required=True,
    help="Blue (initial) wavelength of the interpolation window.",
)
parser.add_argument(
    "--lambda2",
    type=float,
    required=True,
    help="Red (final) wavelength of the interpolation window.",
)
parser.add_argument(
    "--target",
    type=float,
    required=False,
    help="""Target wavelength withitn interpolation value.  If specified, a plot will be
generated showing the effect of the interpolation.
 """,
)
args = parser.parse_args()
### END ARGUMENT PARSING ###


# CODE
# function to calculate interpolated spectrum
def lin_interp_spec(spec, xax, lambda_1, lambda_2, return_idx=True):
    i1 = np.argmin(np.abs(xax - lambda_1))
    i2 = np.argmin(np.abs(xax - lambda_2))
    m = (spec[i2] - spec[i1]) / (xax[i2] - xax[i1])
    a = spec[i1] + spec[i2] - m * (xax[i1] + xax[i2])
    a /= 2.0
    interp_spec = spec.copy()
    interp_spec[i1 : i2 + 1] = m * xax[i1 : i2 + 1] + a
    if return_idx:
        return interp_spec, i1, i2
    else:
        return interp_spec

  
t = Table.read(args.input)
interp_spec, i1, i2 = lin_interp_spec(
    t["flux"], t["lambda"], args.lambda1, args.lambda2
)
old_flux = t["flux"].copy()
t["flux"] = interp_spec
t.write(args.output)

# add information about running this script to the output file
hdu = fits.open(args.output)
hdu[0].header["HISTORY"] = '--- start of sky_continuum_modify.py command ---'
hdu[0].header["HISTORY"] = command
hdu[0].header["HISTORY"] = '--- end of sky_continuum_modify.py command ---'
hdu.writeto(args.output, overwrite=True)

if args.target:
    w = 25  # width in wavelength samples for plot
    plt.axvline(args.target)
    plt.plot(t["lambda"][i1 - w : i2 + w], t["flux"][i1 - w : i2 + w])
    plt.plot(t["lambda"][i1 - w : i2 + w], old_flux[i1 - w : i2 + w])
    plt.savefig(args.output[:-5] + ".png")

# END CODE
