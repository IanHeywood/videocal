import os
import glob

myms = glob.glob('*wtspec.ms')[0]
soloms = myms#.split('/')[-1]
imgname = 'img_'+soloms+'_wsX'
maskname = glob.glob('../../masks/*'+soloms+'*.fits')[0]
print maskname
syscall = 'wsclean -size 12000 12000 -scale 0.7asec -niter 30000 -threshold 1e-6 -gain 0.1 -mgain 0.85 -weight briggs 0.0 -datacolumn DATA -name '+imgname+' -fitsmask '+maskname+' -channelsout 4 -beamsize 4.5 -fit-spectral-pol 3 -joinchannels -mem 90 '+myms
print syscall
os.system(syscall)
