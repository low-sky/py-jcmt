#!/usr/bin/python

import commands
import sys
import pyfits
import matplotlib.pyplot as p
import astropy.io.fits as fits
filenames = sys.argv[1:]
for file in filenames:
    commands.getoutput('rm temp.*')
    print file
    command = 'source $STARLINK_DIR/etc/profile &  $STARLINK_DIR/bin/smurf/makecube specbounds=\\"420 422\\" out=temp.sdf in='+file
    print command
    print commands.getoutput(command)
    command = '$STARLINK_DIR/bin/convert/ndf2fits temp.sdf temp.fits'
    print commands.getoutput(command)
#    hdu = pyfits.open('temp.fits')
#    p.imshow(pyfits.getdata('temp.fits'))
    image = fits.getdata('temp.fits')
    p.imshow(image[0,:,:])
    p.colorbar()
    p.title(r'\verb+'+file+'+')
    # fig.show_colorscale(pmin=0.1,pmax=99.9,cmap='BrBG')
    # fig.add_colorbar()
    # fig.add_grid()
    # fig.grid.set_color('black')
#    fig.add_beam()
#    fig.beam.set_major(14/3.6e3)
#    fig.beam.set_minor(14/3.6e3)
#    fig.axis_labels.set_xtext(file)
    
#    fig.tick_labels.set_font(size='small')
#    fig.axis_labels.set_font(size='small')
#    fig.set_system_latex(True)
#    fig.set_tick_labels_style('latex')
#    fig.set_labels_latex(True)
    p.savefig('./figs/'+file+'.pdf',format='pdf')
    p.close()
    p.clf()
#    img = pyfits.getdata('temp.fits')
#    p.imshow(img[0,:,:],vmin=-4,vmax=4,origin='lower')
#    p.colorbar()
#    p.title(file)
#    p.draw()
#    p.savefig('./figs/'+file+'.png', format='pdf')

