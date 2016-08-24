import re,urllib
sites = ['google','yahoo','CNN', 'TCS']

pat = re.compile(r'<title>+\s*.*\s*</title>+',re.I | re.M)

for s in sites:
    print "Searching: ",s
    try:
        u = urllib.urlopen("http://" +s+ ".com")
    except IOError as e:
        print "Error", e

    text = u.read()
    #print text

    #text = str(text).replace('\n', '').replace('\t','').replace('\r','')
    title = re.findall(pat,str(text))
    #print title
    if(len(title)>0): print title[0]

