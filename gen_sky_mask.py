#! /usr/bin/env python

import argparse
import os
from os.path import basename, dirname
import sys
import numpy as np
from astropy.io import fits
from astropy.stats import sigma_clip
from scipy.ndimage import uniform_filter


def mask_opt(mask, n_iter=5):
    # shrink mask to eliminate solitary pixels
    cond_1 = uniform_filter(mask, size=3) * 9 > 7.5
    np.place(mask, cond_1, 1.0)
    # grow mask unconditionally
    cond_2 = uniform_filter(mask, size=3) * 9 < 8.5
    np.place(mask, cond_2, 0.0)
    # grow mask multiple times with round edge
    for i in range(0, n_iter):
        cond_3 = uniform_filter(mask, size=3) * 9 < 6.5
        np.place(mask, cond_3, 0.0)

    return mask


# store command that was entered by the user
command = os.path.basename(sys.argv[0])
for entity in sys.argv[1:]:
    command = command + " " + entity

parser = argparse.ArgumentParser(
    description="""
Compute sky mask from continuum image.
"""
)
parser.add_argument(
    "-i",
    "--input",
    required=True,
    type=str,
    help="""Name of the input FITS file containing the continuum image.""",
)
parser.add_argument(
    "--sigma",
    required=False,
    type=float,
    default=3.0,
    help="""The number of standard deviations to use for the clipping limit (default: 3)""",
)
parser.add_argument(
    "--niter",
    required=False,
    type=int,
    default=4,
    help="""Number of iterations for final mask dillation (default: 4).""",
)
args = parser.parse_args()

im, head = fits.getdata(args.input, header=True)
head.remove('BUNIT')
head["HISTORY"] = "--- start of gen_sky_mask.py command ---" 
head["HISTORY"] = command                                      
head["HISTORY"] = "--- end of gen_sky_mask.py command ---"   

# sigma clipping & conversion to float
sc_im = sigma_clip(im, sigma=args.sigma)
sc_mask = (~sc_im.mask).astype(float)

orig_mask = sc_mask.copy()
new_mask = mask_opt(sc_mask, n_iter=args.niter)

infile_basename = basename(args.input)
infile_pathname = dirname(args.input)

if infile_pathname == "":
    infile_pathname = "./"

mask_outfile = infile_pathname + '/mask_' + infile_basename
mask_hdu = fits.PrimaryHDU(data=new_mask, header=head)
orig_mask_hdu = fits.ImageHDU(data=orig_mask, header=head)
hdu_list = fits.HDUList([mask_hdu, orig_mask_hdu])
hdu_list.writeto(mask_outfile)

