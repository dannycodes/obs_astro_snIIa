import numpy as np
import os, sys, subprocess
import pyfits
sys.path.insert(0,'./MatchImages')
from MatchImages import *
# Import each gp file and extract the timestamp

image_path = "/home/daniel/Documents/school/Astronomy/final/sn2013aa_rp/"
outdir = "/home/daniel/Documents/school/Astronomy/final/rp_output/"
out_files = "/home/daniel/Documents/school/Astronomy/final/rp_index/"

#List all fits header filenames
image_list = []
for root, dirs, files in os.walk(image_path):
	for filename in files:
		if filename.startswith("._"):
			filename = filename[2:-1]
		if filename.endswith('.fits'):
			image_list.append(root+filename)

#Next, run source extractor on each image. 
#Make sure to make a directory to output the .cat files
try:
    os.mkdir(outdir)
    os.mkdir(out_files)
except OSError as e:
    if e.errno == 17:
        pass
    else:
        raise
catalog_list = []
indexing = []
for index, image_location in enumerate(image_list):
    # if index > 3:
    #     break
    outpath=outdir+image_location.split('/')[-1].replace('.fits','.cat')
    print "Finding stars in "+image_location.split('/')[-1]
    conf_path = './sextractor/sextractor.sex'  # You made need to edit the PARAMETERS_NAME or FILTER_NAME in this file
    subprocess.call(['/usr/bin/sextractor',image_location,'-c', conf_path,'-CATALOG_NAME',outpath])
    if os.path.isfile(outpath):
        catalog_list.append(outpath)
        indexing.append(index)
    else:
        print "Unable to make catalog file"
    print ""

#Finally, run Match_images to match up the stars in each image.
#You'll probably want to match every image with just the first image.
matched_index = []
matched_indexing = []
for index, catalog_location in zip(indexing[1:], catalog_list[1:]):
    outpath=outdir+catalog_list[0].split('/')[-1].split('.')[0]+'_'+catalog_location.split('/')[-1].split('.')[0]+'_matched.cat'
    cat1 = catalog_list[0]
    cat2 = catalog_location
    print "Matching Stars from "+cat1.split('/')[-1]+" and "+cat2.split('/')[-1]

    try:
        ret = MatchImages(cat1,cat2)
        np.savetxt(outpath, ret[0],fmt='%10.3f %10.3f %12s %12s %8.4f %8.4f %8.4f %8.4f %12s %8.3f %8.2f %4i %10.3f %10.3f %12s %12s %8.4f %8.4f %8.4f %8.4f %12s %8.3f %8.2f %4i')
        np.savetxt(outpath.replace(".cat",".dict"), np.asarray(('\n'.join(['%16s::\t%s' % (key, value) for (key, value) in ret[1].items()])))[None],fmt='%s')
        np.savetxt(outpath.replace(".cat",".param"), np.asarray(('\n'.join(['%7s::\t%s' % (key, value) for (key, value) in ret[2].items()])))[None],fmt='%s')
        #Just ignores first image entirely
    except UnboundLocalError:
        print "\tUnable to find matching stars!"
    else:
        matched_index.append(outpath)
        matched_indexing.append(index)
    print '\tDone\n'

# You can also get a list observation times
image_time_list = []
image_indexing = []
for index, image_location in enumerate(image_list):
    image = pyfits.open(image_location)
    # This is the Modified Julian Date of observation
    date_str = image[0].header['MJD-OBS']
    image_time_list.append(float(date_str))
    image_indexing.append(index)
times = np.array(zip(image_indexing, image_time_list), dtype=[('int', int),('float', float)])
matched = np.array(zip(matched_indexing, matched_index), dtype=[('int', int),('str', object)])

np.savetxt(out_files + "times.cat", times, delimiter=" ", fmt=["%d","%f"])
np.savetxt(out_files + "matched.cat", matched, delimiter=" ", fmt=["%d", "%s"])

