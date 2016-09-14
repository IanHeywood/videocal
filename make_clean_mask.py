import random
import string
import os
import sys
import numpy
import pyfits
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-i','--image',dest='inpimg',help='Template image',default='',metavar='FILE')
parser.add_option('-l','--lsm',dest='mylsm',help='Tigger LSM',default='',metavar='FILE')
parser.add_option('-c','--cut',dest='mycut',help='Flux cut for boolean mask',default=0.005)
(options,args) = parser.parse_args()
inpimg = options.inpimg
mylsm = options.mylsm
mycut = float(options.mycut)

importonly = False

def gi(message):
        print '\033[92m'+message+'\033[0m'

def ri(message):
        print '\033[91m'+message+'\033[0m'

def getImageAndPSF(fitsfile):
        input_hdu = pyfits.open(fitsfile)[0]
	hdr = input_hdu.header
	bmaj = hdr.get('BMAJ')
	bmin = hdr.get('BMIN')
	bpa = hdr.get('BPA')
        if len(input_hdu.data.shape) == 2:
                image = numpy.array(input_hdu.data[:,:])
        elif len(input_hdu.data.shape) == 3:
                image = numpy.array(input_hdu.data[0,:,:])
        else:
                image = numpy.array(input_hdu.data[0,0,:,:])
        return image,bmaj*3600.0,bmin*3600.0,bpa

def flushFits(newimage,fitsfile):
        f = pyfits.open(fitsfile,mode='update')
        input_hdu = f[0]
        if len(input_hdu.data.shape) == 2:
                input_hdu.data[:,:] = newimage
        elif len(input_hdu.data.shape) == 3:
                input_hdu.data[0,:,:] = newimage
        else:
                input_hdu.data[0,0,:,:] = newimage
        f.flush()

def tempgen(size=8, chars=string.ascii_uppercase + string.ascii_lowercase):
	return ''.join(random.choice(chars) for _ in range(size))

if not importonly:
	if inpimg == '' or mylsm == '':
		print 'Please specify both required image and LSM'
		sys.exit(-1)
	else:
		inpdata,bmaj,bmin,bpa = getImageAndPSF(inpimg)
		if not os.path.isdir('masks'):
			gi('Creating masks folder')
			os.system('mkdir masks')
		maskfits = 'masks/'+inpimg.replace('.fits','_mask.fits').split('/')[-1]
		gi('Duplicating '+inpimg+' into '+maskfits)
		os.system('cp '+inpimg+' '+maskfits)

		tmpfits = tempgen()+'.fits'
		gi('Duplicating '+inpimg+' into '+tmpfits)
		os.system('cp '+inpimg+' '+tmpfits)
	
		zerodata = inpdata*0.0
		gi('Zeroing '+tmpfits)
		flushFits(zerodata,tmpfits)

		gi('Restoring '+mylsm+' into '+tmpfits)
		syscall = 'tigger-restore --restoring-beam='+str(bmaj*0.6)+':'+str(bmin*0.6)+':'+str(bpa)+' '+tmpfits+' '+mylsm
		os.system(syscall)
		restfits = tmpfits.replace('.fits','.restored.fits')

		gi('Making Boolean mask')		
		modeldata,bmaj,bmin,bpa = getImageAndPSF(restfits)
		maskdata = numpy.array(modeldata > mycut,dtype='double')

		gi('Writing mask image '+maskfits)
		flushFits(maskdata,maskfits)

		gi('Removing '+tmpfits)
		os.system('rm '+tmpfits)

		gi('Removing '+restfits)
		os.system('rm '+restfits)

		gi('Done')
