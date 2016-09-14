import os
import glob

myms = glob.glob('*.ms')[0]

imgname = 'img_'+myms+'_ws_dEresid'
#maskname = glob.glob('../masks/*'+myms+'*.fits')[0]
#print maskname
syscall = 'wsclean -size 12000 12000 -scale 0.7asec -niter 10000 -threshold 10e-7 -gain 0.1 -mgain 0.85 -weight briggs 0.0 -datacolumn CORRECTED_DATA -name '+imgname+' -channelsout 4 -fit-spectral-pol 3 -beamsize 4.5 -joinchannels -mem 90 -no-update-model-required '+myms

print syscall
os.system(syscall)
