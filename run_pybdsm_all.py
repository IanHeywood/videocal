import os
from lofar import bdsm
import glob

fitslist = glob.glob('*dErest*.fits')

def find_sources(infile):
	img = bdsm.process_image(infile,thresh_pix=5.0,thresh_isl=3.0,frequency=1.5e+09)
	img.write_catalog(format='ascii',catalog_type='gaul',clobber=True,incl_empty=True)

for item in fitslist:
	id = item.split('.ms')[0]
	wsX = glob.glob(id+'*wsX*')
	if len(wsX) > 0:
		find_sources(item)
		find_sources(wsX[0])
