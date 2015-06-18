# coding:utf-8
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from model import rss_handler
from supporter import debug_tools
import time
import conf
import chardet


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


server = SimpleXMLRPCServer(("localhost", 10000), requestHandler=RequestHandler)
server.register_introspection_functions()


def demo():
    return "Time now is: {time_now}".format(time_now=time.strftime("%Y %b %d %H:%M:%S", time.localtime()))


server.register_function(demo, 'demo')


class DataHandler():
    def __init__(self):
        self.livedoor_rss_raw = rss_handler.parse_livedoor()
        self.livedoor_rss_for_maintab = {}
        self.re_parse_livedoor_rss_for_maintab()

    def re_parse_livedoor_rss_for_maintab(self):
        self.livedoor_rss_for_maintab = {}
        for each_key in self.livedoor_rss_raw.keys():
            self.livedoor_rss_for_maintab[each_key] = []
            for a_news in self.livedoor_rss_raw[each_key]["entries"]:
                title = a_news["title"].encode("utf8")
                link = conf.news_view_root_url + "?news_id=" + a_news["link"].encode("utf8") \
                                               + "&" + "title=" + title
                self.livedoor_rss_for_maintab[each_key].append((title, link))

    def get_livedoor_rss_for_maintab(self):
        return self.livedoor_rss_for_maintab




data_handler = DataHandler()


def get_livedoor():
    return data_handler.get_livedoor_rss_for_maintab()


server.register_function(get_livedoor, 'get_livedoor')
#
# class RssHandler:
#     def __init__(self):
#         self.livedoor = rss_handler.parse_livedoor()
#
#     # def get_livedoor(self):
#     #     return self.livedoor
#
#     def demo_inclass(self):
#         return "123"
#
#
# server.register_instance(RssHandler())



# Server on
debug_tools.console_print("data_server is ready to go")
server.serve_forever()
