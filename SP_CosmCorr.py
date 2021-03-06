#!/usr/bin/env python

""" SP_CosmCorr - Correct for Cosmic rays
    v1.0: 2018-06-15, mdevogele@lowell.edu
"""

import argparse, shlex

import SP_Toolbox as SP
import numpy as np

from SP_CheckInstrument import CheckInstrument

import SP_diagnostics as diag


from astropy.io import fits

#import cosmic

from astroscrappy import detect_cosmics



def Cosmic(filename,Diagnostic):
    
    Out_Name = []
#    telescope, obsparam = CheckInstrument([filename[0]])
    for idx, elem in enumerate(filename): 
        hdulist = fits.open(elem)
        data=hdulist[0].data
#        c = cosmic.cosmicsimage(data,satlevel=65000)
        
        crmask, c = detect_cosmics(data, inmask=None, satlevel=65000)
        
        
#        c.run(maxiter = 1)
#        hdulist[0].data = c.cleanarray
        hdulist[0].data = c

        Out_Name.append(elem.replace('.fits','').replace('_Procc','') + '_' + '_CosmCorr' + '.fits')
        hdulist.writeto(elem.replace('.fits','').replace('_Procc','') + '_' + '_CosmCorr' + '.fits')
        
    if Diagnostic: 
        diag.create_website('Cosmic-Correction_Log.html')
        diag.add_CosmCorr(Out_Name,'Cosmic-Correction_Log.html')

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Create a log file')

    parser.add_argument('images', help='images to process or \'all\'',
                        nargs='+')
    
    parser.add_argument('-d',
                        help='Enable or disable the diagnostic',
                        action="store_false",
                        default = True)  

    args = parser.parse_args()
    filenames = args.images    
    Diagnostic = args.d
    
    # call run_the_pipeline only on filenames
    Cosmic(filenames,Diagnostic)
    pass
