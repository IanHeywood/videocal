import os
import glob

xx = glob.glob('*.backup')

for item in xx:
	opfits = item.replace('.backup','')
	syscall = 'mv '+item+' '+opfits
	print syscall
	os.system(syscall)