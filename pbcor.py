import glob
import os
import sys
import numpy
import pyfits

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
	pbfits = '../../pbimages/img_sb25575669_VIDEO_XMM1_9s_wtspec.ms_full_pb.fits'
#	pbfits = '../../pbimages/8400/img_sb25575669_VIDEO_XMM1_9s.ms_pbimg.flux.fits'
	gi('Reading '+pbfits)
	pbimg = getImage(pbfits)
	if not os.path.isdir('weights'):
		gi('Creating weights folder')
		os.system('mkdir weights')
	else:
		gi('Found weights folder')
	if not os.path.isdir('pbcor'):
		gi('Creating pbcor folder')
		os.system('mkdir pbcor')
	else:
		gi('Found pbcor folder')
	imglist = glob.glob('*XMM20*.fits')	
	for infits in imglist:
		pbcorfits = 'pbcor/'+infits.replace('.fits','_pbcor.fits')
		if os.path.isfile(pbcorfits):
			ri(pbcorfits+' exists, skipping')
		else:
			wtfits = 'weights/'+infits.replace('.fits','_wt.fits')
			gi('Duplicating '+infits+' into '+pbcorfits)
			os.system('cp '+infits+' '+pbcorfits)
			gi('Duplicating '+infits+' into '+wtfits)
			os.system('cp '+infits+' '+wtfits)
			gi('Reading '+infits)
			img = getImage(infits)
			gi('Writing weight image to '+wtfits)
			wtimg = pbimg**2.0
			flushFits(wtimg,wtfits)
			gi('PB correction')
			pbcorimg = img/pbimg
	                gi('Writing data to '+pbcorfits)
	                flushFits(pbcorimg,pbcorfits)
			gi('Done')
