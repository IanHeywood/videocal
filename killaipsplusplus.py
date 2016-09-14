import random
import os

tmpfile = 'temp_'+str(random.randint(0,10000))+'.txt'
os.system('ps -x | grep casa > '+tmpfile)
f = open(tmpfile)
line = f.readline()
while line:
	pid = line.split()[0]
	print 'Killing',pid
	syscall = 'kill -9 '+pid
	os.system(syscall)
	line = f.readline()
f.close()
os.system('rm '+tmpfile)
