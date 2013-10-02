#!/usr/bin/python

import commands
import sys
import astropy.io.fits as pyfits
import matplotlib.pyplot as p

filenames = sys.argv[1:]

for file in filenames:
    commands.getoutput('rm temp.*')
    outfile = "_blscan.".join(file.rsplit(".", 1))
    command = 'source $STARLINK_DIR/etc/profile &  $STARLINK_DIR/bin/kappa/mfittrend '+file+' out=temp.sdf order=0 axis=1 ranges=\\"240.0 280.00 960.0 1000.0\\"'
    print command
    print commands.getoutput(command)
    command = '$STARLINK_DIR/bin/kappa/sub '+file+' temp.sdf '+outfile
    print commands.getoutput(command)
