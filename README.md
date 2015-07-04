Observation Astronomy: Type 1A Supernova 
========================================
Using data from LOCGT telescope array, we will generate decay curves for each image band. Using these curves, we will determine which element decay paths are being observed, and use this information to determine the nature of the observed phenomena, that being a type 1a supernova. 

The data
--------
Data is seperated into 3 color bands, ip, rp, and gp.

Using the Code
--------------
First run sextraction.py. You will need the sextractor package, and you will need to determine appropriate settings in .param and .sex files. Look in sextraction file for examples. 

Next run parse.py, which will do the heavy lifting of parsing the matched files, correlating them with their times, and then outputing the appropriate images. 

Generated images are in the images dir as an example.

Results 
-------
The .tex of my paper is available in the paper dir.
