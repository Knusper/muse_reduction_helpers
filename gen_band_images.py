#! /usr/bin/env python

import sys
from os import path
from mpdaf.obj import Cube
from astropy import units as u
from astropy.io import fits
from astropy.table import Table

cube_file = sys.argv[1]

# included bands
bands = ["Johnson_V", "Cousins_R", "Cousins_I", "SDSS_g", "SDSS_r", "SDSS_i", "SDSS_z"]

cbe = Cube(cube_file)

band_ims = []
for band in bands:
    print(cube_file + ": Computing " + band)
    im = cbe.get_band_image(band)
    im.data_header["EXTNAME"] = band
    band_ims.append(im)


# Pan-STARS 1 filter curves
script_dir = path.dirname(path.realpath(__file__))
flt_tbl = Table.read(script_dir + "/ps1_flt_crv.fits")
bands = [("PS1_g", "gp1"), ("PS1_r", "rp1"), ("PS1_i", "ip1"), ("PS1_z", "zp1")]
lambdas = flt_tbl["lambda"]
for band in bands:
    print(cube_file + ": Computing " + band[0])
    im = cbe.bandpass_image(lambdas, flt_tbl[band[1]], unit_wave=u.nm)
    im.data_header["EXTNAME"] = band[0]
    band_ims.append(im)


print(cube_file + ": Append images as HDUs to input file...")
hdu_list = fits.open(cube_file, mode="append", save_backup=True)
for band_im in band_ims:
    hdu_list.append(fits.ImageHDU(data=band_im.data.data, header=band_im.data_header))
hdu_list.flush(verbose=True)
