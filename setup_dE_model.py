import numpy
import os
import Pyxis
import Tigger
import glob
import pyfits
import string
import random
from astLib import astWCS
from astLib import astCoords as ac
from lofar import bdsm


#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Function definitions
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


def gi(message):
        print '\033[92m'+message+'\033[0m'


def ri(message):
        print '\033[91m'+message+'\033[0m'


def rad2deg(x):
	return 180.0*x/numpy.pi


def tempname(size=12,chars=string.ascii_uppercase+string.digits+string.ascii_lowercase):
	return ''.join(random.choice(chars) for _ in range(size))


def getfreq(f0,f1,chan,nchan):
	chan = int(chan)
	df = (float(f1) - float(f0))/float(nchan)
	return f0+(chan*df)+(df/2.0)


def tiggerConvert(gaul):
	args = []
	tigger_convert  = Pyxis.x("tigger-convert")
	#Dictionary for establishing correspondence between parameter names in gaul files produced by pybdsm, and pyxis parameter names
	dict_gaul2lsm = {'Gaus_id':'name', 'Isl_id':'Isl_id', 'Source_id':'Source_id', 'Wave_id':'Wave_id', 'RA':'ra_d', 'E_RA':'E_RA', 'DEC':'dec_d', 'E_DEC':'E_DEC', 'Total_flux':'i', 'E_Total_flux':'E_Total_flux', 'Peak_flux':'Peak_flux', 'E_Peak_flux':'E_Peak_flux', 'Xposn':'Xposn', 'E_Xposn':'E_Xposn', 'Yposn':'Yposn', 'E_Yposn':'E_Yposn', 'Maj':'Maj', 'E_Maj':'E_Maj', 'Min':'Min', 'E_Min':'E_Min', 'PA':'PA', 'E_PA':'E_PA', 'Maj_img_plane':'Maj_img_plane', 'E_Maj_img_plane':'E_Maj_img_plane', 'Min_img_plane':'Min_img_plane', 'E_Min_img_plane':'E_Min_img_plane', 'PA_img_plane':'PA_img_plane', 'E_PA_img_plane':'E_PA_img_plane', 'DC_Maj':'emaj_d', 'E_DC_Maj':'E_DC_Maj', 'DC_Min':'emin_d', 'E_DC_Min':'E_DC_Min', 'DC_PA':'pa_d', 'E_DC_PA':'E_DC_PA', 'DC_Maj_img_plane':'DC_Maj_img_plane', 'E_DC_Maj_img_plane':'E_DC_Maj_img_plane', 'DC_Min_img_plane':'DC_Min_img_plane', 'E_DC_Min_img_plane':'E_DC_Min_img_plane', 'DC_PA_img_plane':'DC_PA_img_plane', 'E_DC_PA_img_plane':'E_DC_PA_img_plane', 'Isl_Total_flux':'Isl_Total_flux', 'E_Isl_Total_flux':'E_Isl_Total_flux', 'Isl_rms':'Isl_rms', 'Isl_mean':'Isl_mean', 'Resid_Isl_rms':'Resid_Isl_rms', 'Resid_Isl_mean':'Resid_Isl_mean', 'S_Code':'S_Code', 'Total_Q':'q', 'E_Total_Q':'E_Total_Q', 'Total_U':'u', 'E_Total_U':'E_Total_U', 'Total_V':'v', 'E_Total_V':'E_Total_V', 'Linear_Pol_frac':'Linear_Pol_frac', 'Elow_Linear_Pol_frac':'Elow_Linear_Pol_frac', 'Ehigh_Linear_Pol_frac':'Ehigh_Linear_Pol_frac', 'Circ_Pol_Frac':'Circ_Pol_Frac', 'Elow_Circ_Pol_Frac':'Elow_Circ_Pol_Frac', 'Ehigh_Circ_Pol_Frac':'Ehigh_Circ_Pol_Frac', 'Total_Pol_Frac':'Total_Pol_Frac', 'Elow_Total_Pol_Frac':'Elow_Total_Pol_Frac', 'Ehigh_Total_Pol_Frac':'Ehigh_Total_Pol_Frac', 'Linear_Pol_Ang':'Linear_Pol_Ang', 'E_Linear_Pol_Ang':'E_Linear_Pol_Ang'}

	#Dictionary for classifying a parameter as a general parameter or a polarization-specific parameter
	dict_pol_flag = {'Gaus_id':0, 'Isl_id':0, 'Source_id':0, 'Wave_id':0, 'RA':0, 'E_RA':0, 'DEC':0, 'E_DEC':0, 'Total_flux':0, 'E_Total_flux':0, 'Peak_flux':0, 'E_Peak_flux':0, 'Xposn':0, 'E_Xposn':0, 'Yposn':0, 'E_Yposn':0, 'Maj':0, 'E_Maj':0, 'Min':0, 'E_Min':0, 'PA':0, 'E_PA':0, 'Maj_img_plane':0, 'E_Maj_img_plane':0, 'Min_img_plane':0, 'E_Min_img_plane':0, 'PA_img_plane':0, 'E_PA_img_plane':0, 'DC_Maj':0, 'E_DC_Maj':0, 'DC_Min':0, 'E_DC_Min':0, 'DC_PA':0, 'E_DC_PA':0, 'DC_Maj_img_plane':0, 'E_DC_Maj_img_plane':0, 'DC_Min_img_plane':0, 'E_DC_Min_img_plane':0, 'DC_PA_img_plane':0, 'E_DC_PA_img_plane':0, 'Isl_Total_flux':0, 'E_Isl_Total_flux':0, 'Isl_rms':0, 'Isl_mean':0, 'Resid_Isl_rms':0, 'Resid_Isl_mean':0, 'S_Code':0, 'Total_Q':1, 'E_Total_Q':1, 'Total_U':1, 'E_Total_U':1, 'Total_V':1, 'E_Total_V':1, 'Linear_Pol_frac':1, 'Elow_Linear_Pol_frac':1, 'Ehigh_Linear_Pol_frac':1, 'Circ_Pol_Frac':1, 'Elow_Circ_Pol_Frac':1, 'Ehigh_Circ_Pol_Frac':1, 'Total_Pol_Frac':1, 'Elow_Total_Pol_Frac':1, 'Ehigh_Total_Pol_Frac':1, 'Linear_Pol_Ang':1, 'E_Linear_Pol_Ang':1}

	lines = [line.strip() for line in open(gaul)]

	for line in range(len(lines)):
		if lines[line]:
			if lines[line].split()[0] is not '#': 
				gaul_params = lines[line-1].split()[1:] #Parameter list is last line in gaul file that begins with a '#'
				break

	# Initialize lists for general and polarization parameters 
	lsm_params_general = []
	lsm_params_polarization = []

	for param in gaul_params:
		if dict_pol_flag[param] is 0:
			lsm_params_general.append(dict_gaul2lsm[param])
		if dict_pol_flag[param] is 1:
			lsm_params_polarization.append(dict_gaul2lsm[param])

	general_params_string = ' '.join(lsm_params_general)
	pol_params_string = ' '.join(lsm_params_polarization)

	output = gaul.replace('.gaul','.lsm.html')

	cluster = 80.0

	tigger_convert(gaul,output,"-t","ASCII","--format", general_params_string,
		"-f","--rename",
		"--cluster-dist",cluster,
	#	"--min-extent",MIN_EXTENT,
		split_args=False,
		*args);
	return output


def makesubim(infits,ra,dec,size,outfits):
	# ra,dec,size all in degrees
	syscall = 'mSubimage '+infits+' '+outfits+' '
	syscall+= str(ra)+' '+str(dec)+' '+str(size)+' '
	gi('Writing subim: '+outfits)
	os.system(syscall)
	return outfits


def mosaic_directions(fitslist,outfits):
	gi('Making mosaic of subimages')
	tempdir = tempname()
	gi('Creating '+tempdir+'/repro')
	os.mkdir(tempdir)
	os.mkdir(tempdir+'/repro')
	os.chdir(tempdir)
	for item in fitslist:
		os.symlink('../'+item,item)
	os.system('mImgtbl . images.tbl')
	os.system('mMakeHdr images.tbl template.hdr')
	for item in fitslist:
		os.system('mProject '+item+' repro/'+item+' template.hdr')
	os.chdir('repro')
	os.system('mImgtbl . images.tbl')
	os.system('mAdd images.tbl ../template.hdr '+outfits)
	os.rename(outfits,'../../'+outfits)
	os.chdir('../../')
	if cleanup:
		gi('Removing '+tempdir)
		os.system('rm -rf '+tempdir)
	gi('Written '+outfits)
	return outfits


def makeLSM(infits,mybeam,myfreq):
	img = bdsm.process_image(infits,thresh_pix=9.0,thresh_isl=5.0,beam=mybeam,frequency=myfreq)
	foundsrcs = img.write_catalog(format='ascii',catalog_type='gaul',clobber=True,incl_empty=True)
	gaul = infits.replace('.fits','.pybdsm.gaul')
	oplsm = gaul.replace('gaul','lsm.html')
	if foundsrcs:
		tiggerConvert(gaul)
		if cleanup:
			os.system('rm '+gaul)
			os.system('rm '+gaul.replace('.pybdsm.gaul','.fits.pybdsm.log'))
		gi('Wrote LSM:     '+oplsm)
		return (oplsm,True)
	else:
		ri('No sources found in '+str(infits))
		ri('Could be corrupt image, could be trouble source entering null')
		return (oplsm,False)


def tagsources(inlsm):
	model = Tigger.load(inlsm)
	gi('Reading LSM:   '+inlsm)
	srcs = model.sources
	counter = 0
	for src in srcs:
		src.setTag('dE',True)
		counter += 1
	gi('Tagged:        '+str(counter)+' source(s)')
	model.save(inlsm)


def add_dummy(inlsm):
	dummylsm = '../../dummy.lsm.html'
	gi('Adding dummy:  '+inlsm) 
	dsrc = Tigger.load(dummylsm).sources
	model = Tigger.load(inlsm)
	model.sources.append(dsrc[0])
	model.save(inlsm)


def getImage(fitsfile):
	input_hdu = pyfits.open(fitsfile)[0]
	if len(input_hdu.data.shape) == 2:
	        image = numpy.array(input_hdu.data[:,:])
	elif len(input_hdu.data.shape) == 3:
	        image = numpy.array(input_hdu.data[0,:,:])
	else:
	        image = numpy.array(input_hdu.data[0,0,:,:])
	return image


def flushFits(newimage,fitsfile):
	gi('Flushing:      '+fitsfile)
	f = pyfits.open(fitsfile,mode='update')
	input_hdu = f[0]
	if len(input_hdu.data.shape) == 2:
	        input_hdu.data[:,:] = newimage
	elif len(input_hdu.data.shape) == 3:
	        input_hdu.data[0,:,:] = newimage
	else:
	        input_hdu.data[0,0,:,:] = newimage
	f.flush()


def maskimage(infits,directions,size):
	backup = True
	if backup:
		backupfits = infits+'.backup'
		if not os.path.isfile(backupfits):
			gi('Making backup: '+backupfits)
			os.system('cp '+infits+' '+backupfits)
		else:
			ri(backupfits+' already exists, will not overwrite')
	gi('Reading:       '+infits)
	input_hdu = pyfits.open(infits)[0]
	hdr = input_hdu.header
	WCS = astWCS.WCS(hdr,mode='pyfits')
	deg2pix = 1.0/hdr.get('CDELT2') # declination increment
	if len(input_hdu.data.shape) == 2:
		image = numpy.array(input_hdu.data[:,:])
	elif len(input_hdu.data.shape) == 3:
		image = numpy.array(input_hdu.data[0,:,:])
	else:
		image = numpy.array(input_hdu.data[0,0,:,:])
	dx = dy = extent*deg2pix/2.0
	for ra,dec in directions:
		gi('Direction:     '+str(ra)+' '+str(dec))
		xpix,ypix = WCS.wcs2pix(ra,dec)
		x0 = xpix - dx
		x1 = xpix + dx
		y0 = ypix - dy
		y1 = ypix + dy
		gi('Masking:       '+str(x0)+' '+str(x1)+' '+str(y0)+' '+str(y1))
		image[y0:y1,x0:x1] = 0.0
	flushFits(image,infits)


def predict(msname,imgbase):
	syscall = 'wsclean -predict -channelsout 4 -size 12000 12000 '
	syscall+= '-scale 0.7asec -name '+imgbase+' -mem 90 '
	syscall+= '-predict-channels 4 '+msname
	os.system(syscall)



#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Switches
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

ptg = os.getcwd().split('/')[-1]

if ptg=='VLA1':
	myms = 'sb25575669_VIDEO_XMM1_9s_wtspec.ms'
	imgbase = 'img_sb25575669_VIDEO_XMM1_9s_wtspec.ms_wsZ'
	directions = [(33.999766,-3.738245),(33.798279,-3.718641),(33.750664,-4.053504),(33.968075,-3.997347),(34.272869,-4.381236)]
elif ptg=='VLA2':
	myms = 'sb26433110_VIDEO_VLA2_9s_wtspec.ms'
	imgbase = 'img_sb26433110_VIDEO_VLA2_9s_wtspec.ms_wsX'
	directions = [(35.430779,-4.228162),(34.273427,-4.382260)]
elif ptg=='VLA3':
	myms = 'sb26433436_VIDEO_VLA3_9s_wtspec.ms'
	imgbase = 'img_sb26433436_VIDEO_VLA3_9s_wtspec.ms_wsX'
	directions = [(35.429547,-4.228904),(34.742328,-4.156239)]
elif ptg=='VLA4':
	myms = 'sb26442858_VIDEO_VLA4_9s_wtspec.ms'
	imgbase = 'img_sb26442858_VIDEO_VLA4_9s_wtspec.ms_wsY'
	directions = [(35.429430,-4.228708)]
elif ptg=='VLA5':
	myms = 'sb26443220_VIDEO_XMM5_9s_wtspec.ms'
	imgbase = 'img_sb26443220_VIDEO_XMM5_9s_wtspec.ms_wsX'
	directions = [(35.792996,-4.384744),(35.430084,-4.228310)]
elif ptg=='VLA7':
	myms = 'sb26444068_VIDEO_VLA7_9s_wtspec.ms'
	imgbase = 'img_sb26444068_VIDEO_VLA7_9s_wtspec.ms_wsX'
	directions = [(37.221898,-3.627379),(36.582761,-4.426531)]
elif ptg=='VLA8':
	myms = 'sb26444385_VIDEO_VLA8_9s_wtspec.ms'
	imgbase = 'img_sb26444385_VIDEO_VLA8_9s_wtspec.ms_wsX'
	directions = [(37.221825,-3.627080),(37.597903,-4.207849),(37.315968,-4.704909)]
elif ptg=='VLA9':
	myms = 'sb26444701_VIDEO_VLA9_9s_wtspec.ms'
	imgbase = 'img_sb26444701_VIDEO_VLA9_9s_wtspec.ms_wsX'
	#directions = [(34.170383,-4.734063),(34.046568,-4.434639),(33.587544,-4.370617),(33.750659,-4.895367),(33.746818,-4.968314),(33.301458,-4.955303),(34.274790,-4.380797),(33.750796,-4.053275)] 
	directions = [(34.170542,-4.733622),(33.750416,-4.894096),(34.045412,-4.435080),(33.584862,-4.371759)]
elif ptg=='VLA10':
	imgbase = 'img_sb26445017_VIDEO_VLA10_9s_wtspec.ms_wsY'
	myms = 'sb26445017_VIDEO_VLA10_9s_wtspec.ms'
	directions = [(34.273170,-4.381715),(34.169425,-4.733705),(34.575644,-4.768605)]
elif ptg=='VLA11':
	imgbase = 'img_sb26445333_VIDEO_VLA11_9s_wtspec.ms_wsX'
	myms = 'sb26445333_VIDEO_VLA11_9s_wtspec.ms'
	directions = [(34.665230,-4.696890),(34.575793,-4.768505),(35.429731,-4.228967)]
elif ptg=='VLA12':
	myms = 'sb26445649_VIDEO_XXM12_9s_wtspec.ms'
	imgbase = 'img_sb26445649_VIDEO_XXM12_9s_wtspec.ms_wsZ'
	directions = [(35.429637,-4.227692)]
elif ptg=='VLA13':
	myms = 'sb26445965_VIDEO_VLA13_9s_wtspec.ms'
	imgbase = 'img_sb26445965_VIDEO_VLA13_9s_wtspec.ms_wsX'
	directions = [(35.429399,-4.228957)]
elif ptg=='VLA14':
	myms = 'sb26446281_VIDEO_XMM14_9s_wtspec.ms'
	imgbase = 'img_sb26446281_VIDEO_XMM14_9s_wtspec.ms_wsX'
	directions = [(35.988054,-4.686725),(35.793132,-4.384367)]
elif ptg=='VLA16':
	myms = 'sb26446913_VIDEO_VLA16_9s_wtspec.ms'
	imgbase = 'img_sb26446913_VIDEO_VLA16_9s_wtspec.ms_wsX'
	directions = [(37.316065,-4.703997),(37.221907,-3.626980)]
elif ptg=='VLA17':
	myms = 'sb26447229_VIDEO_VLA17_9s_wtspec.ms'
	imgbase = 'img_sb26447229_VIDEO_VLA17_9s_wtspec.ms_wsX'
	directions = [(34.170175,-4.734457),(33.746535,-4.964289),(34.015305,-5.132701)]
elif ptg=='VLA18':
	myms = 'sb30614885_VIDEO_VLA18_9s_wtspec.ms'
	imgbase = 'img_sb30614885_VIDEO_VLA18_9s_wtspec.ms_wsX'
	directions = [(34.575909,-4.769013),(34.614223,-4.911308)]
elif ptg=='VLA19':
	myms = 'sb26448289_VIDEO_VLA19_9s_wtspec.ms'
	imgbase = 'img_sb26448289_VIDEO_VLA19_9s_wtspec.ms_wsX'
	directions = [(34.987847,-4.796711),(34.724616,-4.793414),(34.665077,-4.696757),(34.575138,-4.769458)]
elif ptg=='VLA20':
	myms = 'sb26448605_VIDEO_XMM20_9s_wtspec.ms'
	imgbase = 'img_sb26448605_VIDEO_XMM20_9s_wtspec.ms_wsX'
	directions = [(35.425289,-4.852768),(35.732425,-5.303662)]
elif ptg=='VLA21':
	myms = 'sb26448921_VIDEO_VLA21_9s_wtspec.ms'
	imgbase = 'img_sb26448921_VIDEO_VLA21_9s_wtspec.ms_wsY'
	directions = [(35.988101,-4.687799),(35.732832,-5.303514)]
elif ptg=='VLA22':
	myms = 'sb26449237_VIDEO_VLA22_9s_wtspec.ms'
	imgbase = 'img_sb26449237_VIDEO_VLA22_9s_wtspec.ms_wsX'
	directions = [(36.635772,-5.224054),(36.240163,-5.282714),(35.987784,-4.686653)]
elif ptg=='VLA23':
	myms = 'sb26449554_VIDEO_VLA23_9s_wtspec.ms'
	imgbase = 'img_sb26449554_VIDEO_VLA23_9s_wtspec.ms_wsX'
	directions = [(36.979006,-4.950508),(36.636377,-5.223225)]
elif ptg=='VLA24':
	myms = 'sb26449919_VIDEO_VLA24_9s_wtspec.ms'
	imgbase = 'img_sb26449919_VIDEO_VLA24_9s_wtspec.ms_wsY'
	directions = [(37.316236,-4.703914),(36.978825,-4.951432)]
elif ptg=='VLA25':
	myms = 'sb26450235_VIDEO_VLA25_9s_wtspec.ms'
	imgbase = 'img_sb26450235_VIDEO_VLA25_9s_wtspec.ms_wsX'
	directions = [(33.622841,-5.294833),(33.708825,-5.697650),(33.746376,-4.969235)]
elif ptg=='VLA27':
	myms = 'sb26450867_VIDEO_VLA27_9s_wtspec.ms'
	imgbase = 'img_sb26450867_VIDEO_VLA27_9s_wtspec.ms_wsX'
	directions = [(34.867870,-5.662980)]
elif ptg=='VLA28':
	myms = 'sb26451183_VIDEO_VLA28_9s_wtspec.ms'
	imgbase = 'img_sb26451183_VIDEO_VLA28_9s_wtspec.ms_wsZ'
	directions = [(35.733227,-5.305224),(34.869184,-5.663273)]
elif ptg=='VLA30':
	myms = 'sb26452907_VIDEO_XMM30_9s_wtspec.ms'
	imgbase = 'img_sb26452907_VIDEO_XMM30_9s_wtspec.ms_wsX'
	directions = [(36.271437,-5.612994),(35.732214,-5.304469)]
elif ptg=='VLA31':
	myms = 'sb26453272_VIDEO_VLA31_9s_wtspec.ms'
	imgbase = 'img_sb26453272_VIDEO_VLA31_9s_wtspec.ms_wsX'
	directions = [(36.636005,-5.224525),(36.271594,-5.612550),(36.529513,-5.536508)]
elif ptg=='VLA32':
	myms = 'sb26453810_VIDEO_VLA32_9s_wtspec.ms'
	imgbase = 'img_sb26453810_VIDEO_VLA32_9s_wtspec.ms_wsX'
	directions = [(36.635725,-5.224349)]
else:
	ri('Check your working directory')
	sys.exit(-1)

gi(myms)
gi(imgbase)

extent = 0.015 # size of subimages and mask
cleanup = True
makelsms = False
maskmodels = False
runwspredict = True

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Guts
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

chan_images = sorted(glob.glob(imgbase+'-000*-image.fits'))
chans = []
for chan_image in chan_images:
	chan = chan_image.split('-')[1]
	if chan not in chans:
		chans.append(chan)
	
if makelsms:
	full_merge_list = []
	for chan_image in chan_images:
		dir_merge_list = []
		for ra,dec in directions:
			# Make thumbnail images around troublemaker
			subim = chan_image.replace('.fits','')+'_'+str(ra)+'_'+str(dec)+'.fits'
			subfits = makesubim(chan_image,ra,dec,extent,subim)
			dir_merge_list.append(subfits)
		full_merge_list.append(dir_merge_list)

	# Merge images
	for dir_merge_list in full_merge_list:
		chan = chans[full_merge_list.index(dir_merge_list)]
		chan_dE_image = imgbase+'_'+chan+'_dE-sources.fits'
		if len(directions) > 1:
			mosaic_directions(dir_merge_list,chan_dE_image)
		else:
			os.rename(dir_merge_list[0],chan_dE_image)
		if cleanup:
			for tempfile in dir_merge_list:
				gi('Removing '+tempfile)
				os.system('rm '+tempfile)

	# Find sources with a high threshold, tag LSMs with 'dE'
	for chan in chans:
		chan_dE_image = imgbase+'_'+chan+'_dE-sources.fits'
		mylsm = makeLSM(chan_dE_image,(0.00125,0.00125,0.0),getfreq(1.0e9,2.0e9,chan,4))
		if mylsm[1]:
			tagsources(mylsm[0])
			add_dummy(mylsm[0])
		else:
			ri('Writing dummy lsm to '+mylsm[0])
			os.system('cp ../../dummy.lsm.html '+mylsm[0])

# Mask the model images around the troublemaker
if maskmodels:
	for chan_image in chan_images:
		mod_image = chan_image.replace('image','model')
		maskimage(mod_image,directions,extent)

# Run wsclean in PREDICT mode on new model images
if runwspredict:
	predict(myms,imgbase)
