import os
import glob

xx = glob.glob('VLA*.fits')

for item in xx:
	opfile = item.replace('.fits','_third.fits')
	os.system('mShrink '+item+' '+opfile+' 3')
	
