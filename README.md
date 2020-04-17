#apiscripts

The files in this repository are just a bunch of simple scripts to communicate with various data portal APIs.


 I) getdata-from-esgf.py --- searches and dowmloads ISIMIP model output from the ESGF data portal
 -------------------------------------------------------------
 Dependencies:
 - python 2.7.9 or higher
 - esgf-pyclient (https://esgf-pyclient.readthedocs.io/en/latest/notebooks/examples/logon.html)
 - myproxyclient
 
Instruction:
(1) Make sure you have python 2.7.9 or above.

(2) Install the esgf api client:
	pip install esgf-pyclient
  
(3) Instal myproxyclient
	pip install MyProxyClient
  
(4) create an account and openID (https://esgf-data.dkrz.de/projects/esgf-dkrz/)

(5) Join download groups by agreeing to data policies: 	
	-go to -->  https://esg.pik-potsdam.de/projects/isimip/
	-click on 'isimp research only' --> agree to conditions
	-click on 'isimp unrestricted' --> agree to conditions
  
(6) Adapt getdata-from-esgf.py to your needs
	- assign your username and password credentials
	- modify the search criteria
	- change permissions if needed:
		chmod 775 getdata-from-esgf.py
  - run and follow instructions :)
      ./getdata-from-esgf.py
