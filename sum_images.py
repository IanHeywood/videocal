import os
import sys
import numpy
import pyfits
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-a','--im1',dest='im1',help='Input image 1',default='',metavar='FILE')
parser.add_option('-b','--im2',dest='im2',help='Input image 2',default='',metavar='FILE')
parser.add_option('-o','--out',dest='op',help='Output image',default='',metavar='FILE')
(options,args) = parser.parse_args()
im1 = options.im1
im2 = options.im2
op = options.op

importonly = False

def gi(message):
        print '\033[92m'+message+'\033[0m'

def ri(message):
        print '\033[91m'+message+'\033[0m'

def getImage(fitsfile):
        input_hdu = pyfits.open(fitsfile)[0]
        if len(input_hdu.data.shape) == 2:
                image = numpy.array(input_hdu.data[:,:])
        elif len(input_hdu.data.shape) == 3:
                image = numpy.array(input_hdu.data[0,:,:])
        else:
                image = numpy.array(input_hdu.data[0,0,:,:])
        return image

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

if not importonly:
	if im1 == '' or im2 == '' or op == '':
		ri('Please specify all required images')
		sys.exit(-1)
	else:
		print 'Adding:'
		gi('    '+im1)
		print 'to:'
		gi('    '+im2)
		im1data = getImage(im1)
		im2data = getImage(im2)
		sumdata = im1data+im2data
		print 'to form:'
		gi('    '+op)
		os.system('cp '+im1+' '+op)
		flushFits(sumdata,op)
