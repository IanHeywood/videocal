import os
import sys
infits = sys.argv[1]
opjpeg = '/nfs/ftp/people/hey036/VIDEO/'+infits+'.jpg'
syscall = 'mJPEG -gray '+infits+' -1e-4 3e-4 -out '+opjpeg
os.system(syscall)
