#!/usr/bin/env python
import sys
import astropy.io.fits as fits
from astropy.coordinates import FK5,SkyCoord
import astropy.units as u
from math import cos

def bary2lsr(hdr):
    """
    Given a FITS header, this function returns the magnitude of the
    correction required to convert velocities in the BARYCENT velocity
    frame into velocities in the LSRK frame.

    This velocity shift should be ADDED to velocities to move from
    BARYCENT -> LSRK and SUBTRACTED to convert LSRK -> BARYCENT

    Definitions taken from:
    http://www.gb.nrao.edu/~fghigo/gbtdoc/doppler.html

    Usage:

    unix> bary2lsr.py fits_file_name.fits
    To convert BARYCENT to LSRK, add 18.0701766541 km / s to the
    velocity.

    python% bary2lsr(hdr)
    18.0701766541 km/ s

    Parameters
    ----------
    hdr : FITS header string

    Returns
    -------
    offset : astropy.units quantity of the magnitude of the velocity
    shift.  
    
    """
    Obs_Direction = SkyCoord(hdr['CRVAL1'],hdr['CRVAL2'],frame='fk5',
                             unit="deg")
    LSR_Direction = SkyCoord("18h03m50.29s +30d00m16.8s",frame='fk5')
    sep = Obs_Direction.separation(LSR_Direction)
    mag = 20*u.km/u.s*cos(sep.value)
    return(mag)

if __name__ == "__main__":
    if len(sys.argv)>1:
        inputfile = sys.argv[1]
        hdr = fits.getheader(inputfile)
        magnitude = bary2lsr(hdr)
        print("To convert BARYCENT to LSRK, add {0} to the velocity.".format(magnitude))
