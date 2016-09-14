from pyrap import tables
import Pyxis
import mqt
import numpy
import glob
import os
import sys
import time

def gi(message):
	print '\033[92m'+message+'\033[0m'

def bi(message):
	print '\033[94m\033[1m'+message+'\033[0m'

def ri(message):
        print '\033[91m'+message+'\033[0m'

def getSpectralInfo(msName):
	t = tables.table(msName+'/SPECTRAL_WINDOW',ack=False)
	nChan = t.getcol('NUM_CHAN')[0]
	chanFreqs = t.getcol('CHAN_FREQ')[0]
	t.done()
	return nChan,chanFreqs

def getDDIDs(msName):
	t = tables.table(msName,ack=False)
	ddids = numpy.unique(t.getcol('DATA_DESC_ID'))
	t.done()
	bi('Spectral windows:')
	bi('     '+str(ddids))
	print ''
	return ddids

def getScans(msName):
	# Returns contiguous blocks of scan numbers as a list of TaQL commands
	scan_groups = []
	scan_group = []
	taqls = []
	scan_list = ''
	t = tables.table(msName,ack=False)
	scancol = t.getcol('SCAN_NUMBER')
	scans = numpy.unique(scancol)
	t.done()
	for i in range(numpy.min(scans),numpy.max(scans)+1):
		if i in scans:
			scan_list+=str(i)+','
		else:
			scan_list+='-'
	print ''
	bi('Contiguous scan TaQLs:')
	for item in scan_list.split('-'):
		xx = item.rstrip(',').split(',')
		taql = 'SCAN_NUMBER > '+str(int(xx[0])-1)+' && SCAN_NUMBER < '+str(int(xx[-1])+1)
		taqls.append(taql)
		bi('     '+taql)
	print ''
	return taqls

def pokeTDLconf(filename,param,value):
	lines = []
	f = open(filename,'r')
	line = f.readline()
	while line:
		lines.append(line.rstrip('\n'))
		line = f.readline()
	f.close()
	f = open(filename,'w')
	for line in lines:
		parts = line.replace(' ','').split('=')
		if parts[0] == param:
			print >>f,parts[0]+' = '+value
		else:
			print >>f,line
	f.close()

mqt.MULTITHREAD = 8
resetgains = False
resetdEs = False
dryrun = False
mysec = 'stefcal_dE'
knownflags = [8,9] # known flagged SPWs

dE_map = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] # solve for dEs on a per SPW basis
si_map = [1,1,1,1,1,1,1,1,1,1,2,2,2,3,3,3] # scale solution intervals across band
lsm_map = [0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3] # index in lsm_list per SPW

base_dE_solint = 36
base_g_solint = 18

mslist = glob.glob('*.ms')
lsmlist = sorted(glob.glob('*.html'))

for myms in mslist:
#	soloms = myms.split('/')[-1]
	soloms = myms
#	mymask = glob.glob('masks/*'+soloms+'*.img')[0]
	bi(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
	bi('MS:  '+myms)
	# CALIBRATE
	scans = getScans(myms)
	ddids = getDDIDs(myms)
	bi('Known flagged:')
	bi('     '+str(knownflags))
	print ''
	bi('dE map:')
	bi('     '+str(dE_map))
	print ''
	spws = []
	for ddid in ddids:
		if ddid not in knownflags:
			spws.append(ddid)
	for scanql in scans:
		bi('Scan block: '+str(scans.index(scanql)))
		for spw in spws:
			i = spw
			j = scans.index(scanql)
			do_dE = dE_map[spw]
			lsm_idx = lsm_map[spw]
			mylsm = lsmlist[lsm_idx]
			g_solint = base_g_solint*si_map[spw]			
                        #scan = scanql+' && DATA_DESC_ID=='+str(spw)
			scan = scanql # use ms_sel.ddid for spw selection
			gainpickle = myms+'/gain_block'+str(j)+'_spw'+str(i)+'.cp'
			dEpickle = myms+'/dE_block'+str(j)+'_spw'+str(i)+'.cp'
			if resetgains:
				os.system('rm '+gainpickle)
				gi('  Removed gain table: '+gainpickle)
			if resetdEs:
				os.system('rm '+dEpickle)
				gi('    Removed dE table: '+dEpickle)
			gi('     Spectral window: '+str(spw))
			gi('                 LSM: '+mylsm)
			gi('                TaQL: '+str(scan))
			gi('          Gain table: '+gainpickle)
			if do_dE == 0:
				gi('            dE table: None -- not solving for dEs')
			else:
				gi('            dE table: '+dEpickle)
			pokeTDLconf('tdlconf.profiles','ms_sel.ms_taql_str',scan)
			if not dryrun:
				try:
					mqt.run(script='calico-stefcal.py',
						job='stefcal',
						section=mysec,
						config='tdlconf.profiles',
						args=['ms_sel.msname='+myms,
							'tiggerlsm.filename='+mylsm,
							#'do_output=CORR_RES',
							# Solution intervals
							#'stefcal_diffgain.timeint='+str(dE_solint),
							'stefcal_gain.timeint='+str(g_solint),
							# Channel selector
							#'ms_sel.ms_channel_end='+str(uc),
							#'ms_sel.ms_channel_start='+str(lc),
							#'ms_sel.ms_channel_step=1',
							#'ms_sel.select_channels=1',
							# Scan selector 
							# args doesn't seem to parse spaces correctly
							#"ms_sel.ms_taql_str='"+scan+"'",
							# Gain table
							'ms_sel.ddid_index='+str(spw),
							'stefcal_diffgain.enabled='+str(do_dE),
							'stefcal_gain.table='+gainpickle,
							'stefcal_diffgain.table='+dEpickle])
				except:
					ri('*** Stefcal failed ***')
					logfile = 'error_'+str(time.time())+'.txt'
					f = open(logfile,'w')
					print >>f,myms
					print >>f,gainpickle
					print >>f,dEpickle
					print >>f,str(spw)
					print >>f,mylsm
					print >>f,scan
					f.close()
		print ''
