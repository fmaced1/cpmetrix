#!/usr/bin/python

import json
import optparse
import datetime

parser = optparse.OptionParser()
parser.add_option('-f', '--jsonfile',
    help="Input file to decode. *Required*", default=False)

options, args = parser.parse_args()
jsonfile = options.jsonfile

with open(jsonfile) as json_data:
	d = json.load(json_data)
	emax = d['emax']
	eslope = d['eslope']
	evalue_max = d['evalue_max']
	t_start = d['t_start']
	try:
    		warn_level = d['warn_level']
	except KeyError as ke:
    		warn_level = '0'
	dmean = d['dmean']
	t_stop = d['t_stop']
	dmax = d['dmax']
	integrity = d['integrity']
	unit = d['unit']
	residue = d['residue']
	emean = d['emean']
	edate = d['edate']
	evalue = d['evalue']
	nd = d['nd']
	ne = d['ne']
	evalue_min = d['evalue_min']
	adjusted_sigma = d['adjusted_sigma']
	t_step = d['t_step']
	try:
        	crit_level = d['crit_level']
	except KeyError as ke:
                crit_level = '0'
	f_of_x_on_date = d['f_of_x_on_date']
	sigma = d['sigma']

	summary_data = 'summary_data'	

	observed_point_start = d["highcharts"][0]['pointStart']
	observed_point_interval = d["highcharts"][0]['pointInterval']
	observed_type = d["highcharts"][0]['type']
	observed_name = d["highcharts"][0]['name']
	xdata_observed = 'x_data_observed'	

	predicted_point_start = d["highcharts"][1]['pointStart']
        predicted_point_interval = d["highcharts"][1]['pointInterval']
        predicted_type = d["highcharts"][1]['type']
        predicted_name = d["highcharts"][1]['name']
	xdata_predicted = 'x_data_predicted'	

	fit_point_start = d["highcharts"][2]['pointStart']
        fit_point_interval = d["highcharts"][2]['pointInterval']
        fit_type = d["highcharts"][2]['type']
        fit_name = d["highcharts"][2]['name']
	xdata_fit = 'x_data_fit'	

	summary_header = [ str(summary_data), str(emax), str(eslope), str(evalue_max),str(t_start), str(dmean), str(t_stop), str(dmax), str(integrity), str(unit), str(residue), str(emean), str(edate), str(evalue), str(nd), str(ne), str(evalue_min), str(adjusted_sigma), str(t_step), str(f_of_x_on_date), str(sigma) ]
	print ",".join(summary_header)

	observed_header = [ str(xdata_observed), str(observed_point_start), str(observed_point_interval), str(observed_type), str(observed_name) ]
	print ",".join(observed_header)
	o_line = 0
	o_interval = int(observed_point_interval / 1000 / 60)
	for xobserved in d["highcharts"][0]['data']:
		if o_line == 0:
			o_data_timestamp = int(str(observed_point_start)[:10])
			o_data_timestamp = o_data_timestamp + 0 * 60
			o_line = 1
		else:
			o_data_timestamp = o_data_timestamp + o_interval * 60
		o_data_time = (datetime.datetime.fromtimestamp(int(o_data_timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
		data_observed = [ str(observed_name), str(o_data_time), str(xobserved), str(warn_level), str(crit_level) ] 
		print ",".join(data_observed)
		
	predicted_header = [ str(xdata_predicted), str(predicted_point_start), str(predicted_point_interval), str(predicted_type), str(predicted_name) ]
	print ",".join(predicted_header)
	p_line = 0
	p_interval = int(predicted_point_interval / 1000 / 60)
	for xpredicted in d["highcharts"][1]['data']:
		if p_line == 0:
                        p_data_timestamp = int(str(predicted_point_start)[:10])
                        p_data_timestamp = p_data_timestamp + 0 * 60
                        p_line = 1
                else:
                        p_data_timestamp = p_data_timestamp + p_interval * 60
                p_data_time = (datetime.datetime.fromtimestamp(int(p_data_timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
		data_predicted = [ str(predicted_name), str(p_data_time), str(xpredicted), str(warn_level), str(crit_level) ]
		print ",".join(data_predicted)
	
	fit_header = [ str(xdata_fit), str(fit_point_start), str(fit_point_interval), str(fit_type), str(fit_name) ]
	print ",".join(fit_header)
	f_line = 0
	f_interval = int(fit_point_interval / 1000 / 60)
	for xfit in d['highcharts'][2]['data']:
		if f_line == 0:
                        f_data_timestamp = int(str(fit_point_start)[:10])
                        f_data_timestamp = f_data_timestamp + 0 * 60
                        f_line = 1
                else:
                        f_data_timestamp = f_data_timestamp + f_interval * 60
                f_data_time = (datetime.datetime.fromtimestamp(int(f_data_timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
		data_fit = [ str(fit_name), str(f_data_time), str(xfit), str(warn_level), str(crit_level) ]
		print ",".join(data_fit)
