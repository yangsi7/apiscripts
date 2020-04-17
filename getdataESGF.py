#! /usr/bin/env python2.7

"""
 Searches and dowmloads sismip model output from the ESGF data portal
 -------------------------------------------------------------
 Dependencies:
 -python 2.7.9 or higher
 -esgf-pyclient (https://esgf-pyclient.readthedocs.io/en/latest/notebooks/examples/logon.html)
 -myproxyclient

Instruction:

(1) Make sure you have python 2.7.9 or above.

(2) installthe esgf api client:
	pip install esgf-pyclient

(3) instal myproxyclient
	pip install MyProxyClient

(4) create an account and openID (https://esgf-data.dkrz.de/projects/esgf-dkrz/)

(5) Join download groups by agreeing to data policies: 	
	-go to -->  https://esg.pik-potsdam.de/projects/isimip/
	-click on 'isimp research only' --> agree to conditions
	-click on 'isimp unrestricted' --> agree to conditions

(6) Adapt this script (getdata-from-esgf.py)
	- assign your username and password credentials
	- modify the search criteria
	- change permissions if needed:
		chmod 775 getdata-from-esgf.py
"""

from pyesgf.search import SearchConnection
import tempfile
from pyesgf.logon import LogonManager
import os, subprocess

#--- input user credential --
username='modifyMe'
password='modifyMe'
#---------------------------- 

#--- input search criteria --
project='ISIMIP2b'
model='GFDL-ESM2M'
impact_model='WaterGAP2'
experiment ='rcp45'
variable='Discharge'


def main():
    #--- input user credential --
    username='ocean'
    password='8unTg!S3bh@jhwC'
    #----------------------------
    
    #--- input search criteria --
    project='ISIMIP2b'
    model='GFDL-ESM2M'
    impact_model='WaterGAP2'
    experiment ='rcp45'
    variable='Discharge'

    # Loging in
    lm = LogonManager()
    lm.logoff()
    lm.is_logged_on()
    OPENID = 'https://esgf-data.dkrz.de/esgf-idp/openid/'+username
    myproxy_host = 'esgf-data.dkrz.de'
    lm.logon_with_openid(openid=OPENID, password=password, bootstrap=True)
    lm.logon(hostname=myproxy_host,interactive=False, username=username,password=password,bootstrap=True)
    lm.is_logged_on()
    
    # Open connection with potsam node (ISIMIP) 
    conn = SearchConnection('http://esg.pik-potsdam.de/esg-search', distrib=False)
    
    # Search datasets
    # can do general searches e.g., search for all datasets in ISIMIP2b with experiment='rcp45'. This will return all instances in ctx
    ctx = conn.new_context(
        project=project,
        model=model,
        impact_model=impact_model,
        experiment=experiment,
        variable_long_name=variable)
    
    # list number of counts
    print('Founds '+str(ctx.hit_count)+' matching datasets')
    
    # grab search results and display them
    a=ctx.search()
    cnt=1
    for i in a :
       print('['+str(cnt)+']'+'   ----->  '+i.dataset_id)
       print('- - - - - - - - - - - - - - - - - - - - - - - -')
       cnt = cnt + 1
    
    # Ask user to choose a dataset or to download all 
    num = input("Which one should I download master? [Type -1 for all, 3 for third listed dataset.]")
    
    # Case where user select a specific dataset
    if num != -1:
        print("Downloading dataset "+str(num)+".")
        wget_makeNrun(a[num-1].file_context())
    # case where user selects all
    elif num == -1:
        print("Downloading all "+str(ctx.hit_count)+" datasets.")
        for i in a:
            print("Downloading all datasets returned in search.")
            wget_makeNrun(i.file_context())
    return 0

# Function which create and runs bash wget scripts.
def wget_makeNrun(srch):
    fc = srch
    wget_script_content = fc.get_download_script()
    script_path = tempfile.mkstemp(suffix='.sh', prefix='download-')[1]
    fd = os.open(script_path, os.O_WRONLY)
    os.write(fd,wget_script_content)
    os.close(fd)
    os.chmod(script_path, 0o750)
    download_dir = os.path.dirname(script_path)
    print("Running generated wget-script. Download directory: "+download_dir+'/')
    os.system('bash '+script_path)
    print("done")

if __name__ == "__main__":
    main()
