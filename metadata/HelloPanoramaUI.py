import re,urllib
#sites = ['https://uat1.panoramaadviser.com.au']
sites = ['http://www.google.com']
#proxies = {'http': 'http://L083646:TCS#1981@secure-proxy.btfin.com:8080'}
proxies = {'http': 'http://gatehousek1.stgeorge.com.au:8080'}
#gatehousek1.stgeorge.com.au:8080

pat = re.compile(r'<title>+\s*.*\s*</title>+',re.I | re.M)


for s in sites:
    print "Searching: {} using proxy {}".format(s,proxies['http'])
    try:

        #u = urllib.urlopen(s,proxies=proxies)
        u = urllib.urlopen(s)
    except IOError as e:
        print "Error", e
        exit(-1)

    text = u.read()
    #print text

    #text = str(text).replace('\n', '').replace('\t','').replace('\r','')
    title = re.findall(pat,str(text))
    #print title
    if(len(title)>0): print title[0]

