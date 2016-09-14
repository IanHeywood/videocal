import numpy
import Tigger
import glob

xx = glob.glob('*VLA18*.html')

for mylsm in xx:
	oplsm = mylsm.replace('.lsm.html','_unity.lsm.html')
	print mylsm
	model = Tigger.load(mylsm)
	for src in model.sources:
		src.flux.I = 1.0
	model.save(oplsm)
