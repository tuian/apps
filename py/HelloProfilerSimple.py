#python -m cProfile -o out.prof HelloProfilerSimple.py
#snakeviz out.prof
#python pycallgraph graphviz -- C:\apps\apps\py\HelloProfilerSimple.py
#python pycallgraph -v graphviz -- C:\apps\apps\py\HelloProfilerSimple.py
#C:\Python27\Scripts\pycallgraph.png
'''
From: C:\Python27\Scripts>
python pycallgraph -v graphviz --output-file=HelloProfilerSimple.png -- C:\apps\apps\py\HelloProfilerSimple.py
--output-file=setup.png

python pycallgraph -v graphviz --output-file=XSDFields_Matching.png -- C:\apps\apps\metadata\XSDFields_Matching.py
python pycallgraph -v --max-depth 1 graphviz --output-file=XSDFields_Matching.png -- C:\apps\apps\metadata\XSDFields_Matching.py
python pycallgraph -h, --help

'''
import time
# from HelloPandas import *

def HelloWorld():
    time.sleep(1)

    print "Hello World"

def foo():
    for i in range(10001):
        i= i*i*i

def foo1():
    for i in range(10001):
        i3= i*i*i
        #print "I= {}, I3={}".format(i,i3)

HelloWorld()
foo()
foo1()