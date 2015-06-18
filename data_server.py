# coding:utf-8
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from model import rss_handler
from supporter import debug_tools
import time

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

server = SimpleXMLRPCServer(("localhost", 10000), requestHandler=RequestHandler)
server.register_introspection_functions()

def demo():
    return "Time now is: {time_now}".format(time_now=time.strftime("%Y %b %d %H:%M:%S", time.localtime()))
server.register_function(demo, 'demo')



class MyFuncs:
    pass
server.register_instance(MyFuncs())

# Server on
debug_tools.console_print("data_server is ready to go")
server.serve_forever()