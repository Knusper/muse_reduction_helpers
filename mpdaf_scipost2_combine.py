#! /usr/bin/env python

import argparse
from glob import glob
from mpdaf.obj import CubeList

parser = argparse.ArgumentParser(
    description="""Takes *scipost_2_DATACUBE_FINAL.fits files and passes them through
mpdaf's CubeList.combine for cube combination with sigma-clipping."""
)
parser.add_argument(
    "-d",
    "--directory",
    required=True,
    type=str,
    help="Directory where *scipost_2_DATACUBE_FINAL.fits files are stored.",
)
parser.add_argument(
    "--nmax",
    default=2,
    type=int,
    required=False,
    help="Maxium number of clipping iterations (default: 2).",
)
parser.add_argument(
    "--nclip",
    default=5.0,
    type=float,
    required=False,
    help="Sigma value at which to clip (default: 5).",
)
parser.add_argument(
    "--mad",
    action="store_true",
    required=False,
    help="Use MAD statistics for sigma-clipping.",
)

args = parser.parse_args()

outfile = args.directory + "/DATACUBE_scipost_2_mpdaf_cmbd.fits"
expmapfile = args.directory + "/EXPMAP_scipost_2_mpdaf_cmbd.fits"
statpixfile = args.directory + "/STATPIX_scipost_2_mpdaf_cmbd.fits"


filelist = glob(args.directory + "/*scipost_2_DATACUBE_FINAL.fits")
cubelist = CubeList(filelist)

combined_cube, expmap, statpix = cubelist.combine(
    nmax=args.nmax, nclip=args.nclip, mad=args.mad
)

combined_cube.write(outfile)
print("MPDAF combined cube written to: " + outfile)
expmap.write(expmapfile)
print("Exposure map written to: " + expmapfile)
statpix.write(statpixfile)
print("Statpix table written to: " + statpixfile)
