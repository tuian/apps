from pycallgraph import PyCallGraph,Config,GlobbingFilter
from pycallgraph.output import GraphvizOutput
#http://pycallgraph.slowchop.com/en/master/examples/basic.html

import cProfile
import time
import yappi

def HelloWorld():
    time.sleep(1)
    foo()
    print "Hello World"

def foo():
    for i in range(100):
        pass

# cProfile
# pr = cProfile.Profile()
# pr.enable()
# HelloWorld()
# pr.disable()
# # after your program ends
# pr.print_stats(sort="calls")



# Yappi

# yappi.start()
# foo()
# HelloWorld()
# yappi.get_func_stats().print_all()


# def Test_Main():
#     output_folder = 'c:/apps/apps/graphviz/output/'
#     graphviz = GraphvizOutput()
#     graphviz.output_file = output_folder+'HelloProfiler.png'
#
#     with PyCallGraph(output=graphviz):
#         HelloWorld()
#

#
# if __name__ == '__main__':
#     Test_Main()

# graphviz_output_folder = 'c:/apps/apps/graphviz/output/'
# graphviz = GraphvizOutput()
# graphviz.output_file = graphviz_output_folder+'HelloProfiler.png'
#
# config = Config()
# config.max_depth = 10
# config.trace_filter = GlobbingFilter(exclude=[
#     'pycallgraph.*',
#     'foo',
# ])
#
# with PyCallGraph(output=graphviz,config=None):
#     HelloWorld()

HelloWorld()
