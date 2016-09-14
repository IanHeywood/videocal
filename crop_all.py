import glob
import os

xx = glob.glob('*.jpg')

for infile in xx:
	outfile = infile.replace('.jpg','_crop.jpg')
	print infile,'-->',outfile
	syscall = '/usr/bin/convert '+infile+' -gravity Center -crop 4250x4250+0+0 +repage '+outfile
	os.system(syscall)
	os.system('rm '+infile)
