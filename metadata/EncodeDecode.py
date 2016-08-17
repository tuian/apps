import base64

password = base64.b64encode("TCS#2305")
print "encoded : ", password

password = base64.b64decode("VENTIzIzMDU=")

print "decoded : ", password