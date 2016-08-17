"""
import requests
from requests_ntlm import HttpNtlmAuth
"""



from sharepoint import SharePointSite, basic_auth_opener


#http://sharepoint.btfin.com/it/home/itpm/PST/TCSTeam/Panorama/MDR/


site_url = "http://sharepoint.btfin.com/it/home/itpm/PST/TCSTeam/Panorama/MDR/"

print site_url



#requests.get("http://sharepoint-site.com", auth=HttpNtlmAuth('DOMAIN\\USERNAME','PASSWORD'))
"""
opener = basic_auth_opener(site_url, "L083646", "TCS#3160")
site = SharePointSite(site_url, opener)

for sp_list in site.lists:
    print sp_list.id
"""