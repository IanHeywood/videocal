import Pyxis
import glob

def tiggerConvert(gaul):
	args = []
	tigger_convert  = x("tigger-convert")
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

	cluster = 30.0

	tigger_convert(gaul,output,"-t","ASCII","--format", general_params_string,
		"-f","--rename",
		"--cluster-dist",cluster,
	#	"--min-extent",MIN_EXTENT,
		split_args=False,
		*args);
	return output

gaullist = glob.glob('*.gaul')

for infile in gaullist:
	if os.path.isfile(infile.replace('.gaul','.lsm.html')):
		print 'Skipping',infile
	else:
		tiggerConvert(infile)
