from bs4 import BeautifulSoup
soup = BeautifulSoup(open("accountsandbillers.html"),"lxml")
#print(soup.prettify())

#print soup.name

tag = soup.div.value
#print tag
#print type(tag)
#print tag.name
#print tag.attrs
#print tag.attrs['data-component-name']
#print tag.attrs['data-view-component']
#print tag.string
#print tag

""""""
for dc_name in soup.find_all('div'):
    if ((dc_name.get('data-view-component') != None)):
        if (dc_name.get('data-view-component') != 'messagealert'):
            if (dc_name.get('data-view-component') != 'button'):
                print dc_name.get('data-component-name'),",",dc_name.get('data-view-component')


for dc_name in soup.find_all('span'):
    if ((dc_name.get('data-name') != None)):
        print dc_name.get('data-name'),",","spanDataname"



"""
a = soup.find_all('div')
for divs in a:
    #print divs
    for child in divs.descendants:
     print(child)
"""