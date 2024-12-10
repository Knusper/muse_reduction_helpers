#! /usr/bin/env python

import argparse
from glob import glob
from mpdaf.obj import CubeList

parser = argparse.ArgumentParser(
    description="""Takes *scipost_<run?_DATACUBE_FINAL.fits files and passes them through
mpdaf's CubeList.combine for cube combination with sigma-clipping."""
)
parser.add_argument(
    "-d",
    "--directory",
    required=True,
    type=str,
    help="""Directory where *scipost_<run>_DATACUBE_FINAL.fits files are stored;
    <run> indicates the number of the iteration (default: 2).
""",
)
parser.add_argument(
    "--run",
    required=False,
    type=str,
    default="2",
    help="Scipost run to combine (default: 2).",
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

outfile = args.directory + "/DATACUBE_scipost_" + args.run + "_mpdaf_cmbd.fits"
expmapfile = args.directory + "/EXPMAP_scipost_" + args.run + "_mpdaf_cmbd.fits"
statpixfile = args.directory + "/STATPIX_scipost_" + args.run + "_mpdaf_cmbd.fits"

filelist = glob(args.directory + "/*scipost_" + args.run + "_DATACUBE_FINAL.fits")
print(filelist)
cubelist = CubeList(filelist)

combined_cube, expmap, statpix = cubelist.combine(
    nmax=args.nmax, nclip=args.nclip, mad=args.mad
)

combined_cube.write(outfile)
print("MPDAF combined cube written to: " + outfile)
expmap.write(expmapfile)
print("Exposure map written to: " + expmapfile)
statpix.write(statpixfile, overwrite=True)
print("Statpix table written to: " + statpixfile)
