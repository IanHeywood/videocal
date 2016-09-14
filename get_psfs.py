import pyfits
import numpy
import glob
import pylab

mas = []
mis = []
pas = []

def getCleanBeam(fitsfile):
        input_hdu = pyfits.open(fitsfile)[0]
        hdr = input_hdu.header
        bmaj = hdr.get('BMAJ')
        bmin = hdr.get('BMIN')
        bpa = hdr.get('BPA')
        return (bmaj*3600.0,bmin*3600.0,bpa)

xx = glob.glob('*.fits')

for item in xx:
	bmaj,bmin,bpa = getCleanBeam(item)
	mas.append(bmaj)
	mis.append(bmin)
	pas.append(bpa)
	print item,bmaj,bmin,bpa

mas = numpy.array(mas)
mis = numpy.array(mis)

print numpy.mean(mas),numpy.mean(mis),numpy.mean(pas)
print numpy.std(mas),numpy.std(mis),numpy.std(pas)
