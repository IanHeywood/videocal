from multiprocessing import Pool
import os
import glob

def fits2jpeg(inputimg):
	outputjpeg = 'jpegs/'+inputimg.rstrip('.fits')+'.jpg'
	cmd = 'mJPEG -gray '+inputimg+' -5e-5 5e-4 -out '+outputjpeg
	os.system(cmd)
	print cmd

if __name__ == '__main__':
	fitslist = []
	xx = glob.glob('*.fits')
	for item in xx:
		inputimg = item
		outputjpeg = 'jpegs/'+item.rstrip('.fits')+'.jpg'
		if os.path.exists(outputjpeg):
			print outputjpeg,'exists, skipping'
		else:
			fitslist.append(inputimg)
	pool = Pool(processes=12)
	pool.map(fits2jpeg,fitslist)
