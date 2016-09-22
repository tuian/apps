'''
References:
http://www.python-course.eu/numpy.php

for scipy need Anaconda distribution

'''


import numpy as np

array_Temperatures = np.arange(10)
print array_Temperatures

cvalues = [25.3, 24.8, 26.9, 23.9]
C = np.array(cvalues)

#print cvalues
#print C

print [ x*9/5 + 32 for x in cvalues]
print (C * 9 / 5 + 32)


