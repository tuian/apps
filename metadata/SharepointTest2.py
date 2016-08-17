"""
import requests
from requests_ntlm import HttpNtlmAuth

site_url = "http://sharepoint.btfin.com/it/home/itpm/PST/TCSTeam/Panorama/MDR/"
username =''
password = ''

#requests.get("http://sharepoint-site.com", auth=HttpNtlmAuth('DOMAIN\\USERNAME','PASSWORD'))

requests.get(site_url, auth=HttpNtlmAuth(username,password))
"""

import requests
from sharepoint import SharePointSite

#from requests.auth import HTTPBasicAuth
from requests_ntlm import HttpNtlmAuth
site_url = "http://sharepoint.btfin.com/it/home/itpm/PST/TCSTeam/Panorama/MDR"
#site_url = "http://www.google.com"
username ='AUAUTD0001\L083646'
password = 'TCS#3160'

#r = requests.get(site_url, auth=HTTPBasicAuth(username, password))
r = requests.get(site_url, auth=HttpNtlmAuth(username, password))

#opener = basic_auth_opener(site_url, "L083646", "TCS#3160")
#opener = basic_auth_opener(site_url, "L083646", "TCS#3160")

site = SharePointSite(site_url, r)
#print site.lists
#sp_list = site.lists['ListName']
#for sp_list in site.lists:
#    print sp_list.id

print r.status_code
print r.content
