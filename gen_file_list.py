from astropy.io import fits
from astropy.time import Time

def gen_file_list(files, keyword, value, times=True):
    file_list = []
    time_list = []
    for filename in files:
        header = fits.getheader(filename, 0)
        try:
            if header[keyword] == value:
                file_list.append(filename)
                if times:
                    time_list.append(header['DATE-OBS'])
        except KeyError:
            pass
    if times:
        return file_list, Time(time_list, format='fits')
    else:
        return file_list

