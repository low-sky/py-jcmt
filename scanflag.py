#!/usr/bin/python

import commands
import sys
import astropy.io.fits as fits
import matplotlib.pyplot as p
import numpy as np
import starlink.ndfpack as ndf
import statsmodels.api as sm

filenames = sys.argv[1:]
trim = 64
def mad(array):
    medarray = np.median(array)
    mad = np.median(np.abs(array-medarray))/0.67
    return mad



for file in filenames:
    outfile = "_scanflag.".join(file.rsplit(".", 1))
    print(commands.getoutput('rm temp.*'))
    print(commands.getoutput('rm /var/tmp/*.sdf'))
# Convert SDF file to a shadow file
    s = ndf.Ndf(file)
    data = s.data
    shape = data.shape
    hd = s.head
    print(shape)
    arraymad = mad(data)
    tsys = hd['ACSIS']['TSYS']
    times = hd['JCMTSTATE']['TCS_TAI']
    deltat =  np.median((times-np.roll(times,1)))*86400


    fitshdr = hd['FITS']
    tempfile = open('temp.txt','w')
    for line in fitshdr:
        tempfile.write(line+'\n')
    tempfile.close()
    hddict = fits.Header()
    hddict.fromTxtFile('temp.txt')
    dnu = hddict['IFCHANSP']

    print(dnu,deltat)
    print(tsys.shape)
    ratio = np.zeros((data.shape[0],data.shape[1]))
    for scan in np.arange(data.shape[0]):
         for receptor in np.arange(data.shape[1]):
             spectrum = data[scan,receptor,trim:(-trim)]
             meanval = np.median(spectrum)
             spectrum = spectrum-meanval
#             xvals = np.linspace(-1,1,len(spectrum))
#             regression = sm.RLM(spectrum,xvals, M=sm.robust.norms.HuberT(0.05))
#             spectrum = spectrum-regression.fit().params[0]*xvals
             obs_rms = np.sqrt(np.mean(spectrum[np.abs(spectrum)<100]**2))
             theory_rms = tsys[scan,receptor]/np.sqrt(dnu*deltat)
             ratio[scan,receptor] = obs_rms/theory_rms

#             madspec = mad(spectrum)
# #            print(scan,receptor,madspec,arraymad)
#             if madspec>(1.5*arraymad):
#                 print(scan,receptor)
    mask = np.zeros((data.shape[0],data.shape[1])).astype('b1')
    for receptor in np.arange(data.shape[1]):
        vals = ratio[:,receptor]
        medval = np.median(vals)
        madval = mad(vals)
        mask[:,receptor] = ((vals-medval)>2*madval)*(np.isfinite(ratio[:,receptor]))

    command = 'cp '+file+' /var/tmp/temp_in.sdf'
    print(commands.getoutput(command))
    for scan in np.arange(data.shape[0]):
        for receptor in np.arange(data.shape[1]):
            if mask[scan,receptor]:
                command = "$STARLINK_DIR/bin/kappa/chpix /var/tmp/temp_in.sdf /var/tmp/temp_out.sdf newval=bad section=\\',"+str(receptor+1)+','+str(scan+1)+"\\'"
                print(command)
                commands.getoutput(command)
                command ='mv -f /var/tmp/temp_out.sdf /var/tmp/temp_in.sdf'
                commands.getoutput(command)
    command='mv -f /var/tmp/temp_in.sdf '+outfile
    print(commands.getoutput(command))
