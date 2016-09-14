from multiprocessing import Pool
import os
import glob

#mProject imgPTG464.pbcor.image.tt0.fits repro/imgPTG464.pbcor.image.tt0.repro.fits template.hdr

def reprofits(inpimages):
	inpimg = inpimages[0]
	wtimg = inpimages[1]
	outputimg = 'repro/'+inpimg.rstrip('.fits')+'.repro.fits'
	if os.path.exists(outputimg):
#		print outputimg,'exists, skipping'
		print ''
	else:
		cmd = 'mProject -w '+wtimg+' '+inpimg+' '+outputimg+' template.hdr'
		print inpimg,'--->',outputimg,'(weights: '+wtimg+')'
		print cmd
		os.system(cmd)

if __name__ == '__main__':
	fitslist = sorted(glob.glob('img*.fits'))
#	weightlist = sorted(glob.glob('weights/*.var.tt0.fits'))
	imagepairs = []
	for i in range(0,len(fitslist)):
		ptg = fitslist[i].split('9s')[0]
		print ptg
		wt = glob.glob('weights/'+ptg+'*wt.fits')[0]
		imagepairs.append((fitslist[i],wt))
	for i in range(0,len(fitslist)):
		print imagepairs[i]
	pool = Pool(processes=3)
	pool.map(reprofits,imagepairs)
