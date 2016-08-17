import urllib2
site_url = "http://sharepoint.btfin.com/it/home/itpm/PST/TCSTeam/Panorama/MDR/"

f = urllib2.urlopen('http://www.python.org/')
#f = urllib2.urlopen(site_url)

print f.read(100)
