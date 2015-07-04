import numpy as np
import os 
import matplotlib.pyplot as plt
import datetime
import jdcal

def start():
	for each_file, color in zip(["rp_index","ip_index","gp_index"],['b+','r+','g+']):
		matched = np.loadtxt(each_file+"/matched.cat", dtype=[('int', int),('str', object)])
		times = np.loadtxt(each_file+"/times.cat", dtype=[('int', int),('float', float)])
		first_time = times[0][1]
		data = order_time_matched(matched, times)
		results = runtime(data, first_time)
		refs, mags, dates, k = results["ref_stars"],results["mags"],results["dates"],results["k"]
		adj_mags = normalize(k, refs, mags)
		adj_times_list = [i - 56330 for i in dates]

		print each_file + " successfully parsed: plotting"
		plt.figure()	
		plt.ylim(20,9)  
		plt.plot(adj_times_list, adj_mags, color)
	plt.show()

def order_time_matched(matched, times):
	data = []
	for i in matched:
		for j in times:
			if i[0] == j[0]:
				data.append([i[1],j[1]])
	return data

def runtime(data, first_time):
	mags = []
	times_list = []
	ref_star_list = []
	k_holder = []
	for index, d in enumerate(data):
		# extract data, get x,y coords
		img_data = np.loadtxt(d[0])
		xs = img_data[:,0]
		ys = img_data[:,1]
		print index

		if index==28:
			continue
		if index==58:
			continue
		if index==64:
			continue
		locs = get_locs_of_star(xs, ys)
		if index == 0:
			
			#Get first image mag
			mag_col_0 = img_data[:,4]
			response = get_mags_and_refs(mag_col_0,locs)
			mag = response['magnitude']
			ref_stars = response['ref_stars']
			mags.append(mag)
			ref_star_list.append(ref_stars)
			times_list.append(first_time)
			#Get sky-map diff
			k = net_intensity(ref_stars)
		mag_col = img_data[:,16]
		res = get_mags_and_refs(mag_col, locs)
		mag_sn = res['magnitude']
		ref_stars = res['ref_stars']

		mags.append(mag_sn)
		ref_star_list.append(ref_stars)
		time = d[1]
		times_list.append(time)
	print "finished runtime, onto corrections"
	return {'mags' : mags, 'dates' : times_list, 'ref_stars' : ref_star_list, 'k' : k}

def normalize(k,ref_stars,mags):
	adj_mags = []	
	# Get time averaged values
	averages = []
	for index in range(5):
		s = [ref_stars[i][index] for i in range(len(ref_stars))]
		s_t_avg = sum(s)/ float(len(s))
		averages.append(s_t_avg)
	
	for sn, ref_star in zip(mags, ref_stars):
		time_avg_differences = []
		for star, avg in zip(ref_star, averages):
			difference = star - avg
			time_avg_differences.append(difference)
		normed_difference = sum(time_avg_differences) / len(time_avg_differences)
		corrected_sn_mag = sn - normed_difference
		true_mag = corrected_sn_mag + k
		adj_mags.append(true_mag)
	return adj_mags

def get_locs_of_star(xs, ys):
	for loc, x, y in zip(np.arange(xs.size),xs,ys):
		# Finding the SuperNova itself
		if abs(1050.247 - x) < 1 and abs(1050.652 - y) < 1:
			sn = loc
		# index location of the first star we are using for bg comparison
		if abs(889.4 - x) < 1 and abs(1151.26 - y) < 1:
			s2 = loc
		if abs(860.716 - x) < 1 and abs(1091.42 - y) < 1:
			s3 = loc
		if abs(1189.219 - x) < 1 and abs(1136.96 - y) < 1:
			s4 = loc
		if abs(1167.858 - x) < 1 and abs(1061.484 - y) < 1:
			s5 = loc
		if abs(936.62- x) < 1 and abs(906.9- y) < 1:
			s6 = loc
	return [sn,s2,s3,s4,s5,s6]

def get_mags_and_refs(col, li):
	sn_mag  = col[li[0]]
	s2_mag = col[li[1]]
	s3_mag = col[li[2]]
	s4_mag = col[li[3]]
	s5_mag = col[li[4]]
	s6_mag = col[li[5]]
	magnitude = sn_mag
	ref_stars = [s2_mag, s3_mag, s4_mag, s5_mag, s6_mag]
	return {'magnitude' : magnitude, 'ref_stars' : ref_stars }

def net_intensity(refs):
	# Find k (relate sky-map to data	)
	# Define list of values from sky maps for the stars, arranged as s2 -> s6
	sky_map = [15.9, 14.55, 14.35, 14.4, 13.9]
	sky_map_avg = sum(sky_map) / float(5)
	local_star_avg = sum(refs) / float(5)
	k = abs(sky_map_avg - local_star_avg)
	return k

start()
