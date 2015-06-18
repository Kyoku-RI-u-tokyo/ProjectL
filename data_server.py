# coding:utf-8
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from model import rss_handler
from model import content_handler
from supporter import debug_tools
import time
import conf

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
        self.rss_all = rss_handler.parse_all()

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

    def get_best_n_match_news(self, news, n=3):
        def compare_by_distance(x, y):
            pivot = news.get_simhash_value()
            return content_handler.cal_hamming_distance(x.get_simhash_value(), pivot)\
                   -content_handler.cal_hamming_distance(y.get_simhash_value(), pivot)

        result = []
        for each in sorted(self.rss_all.values(), cmp=compare_by_distance):
            if len(result) >= 3:
                break
            elif each.get_id() != news.get_id():
                result.append(each)
        # print(news)
        # print("="*10)
        # for each in result:
        #     print each
        #     print content_handler.cal_hamming_distance(news.get_simhash_value(), each.get_simhash_value())
        # return result
        return result


data_handler = DataHandler()


def get_livedoor():
    return data_handler.get_livedoor_rss_for_maintab()
server.register_function(get_livedoor, 'get_livedoor')

def get_best_n_match(news_id, n=3):
    result = []
    for each in data_handler.get_best_n_match_news(data_handler.rss_all[news_id], n):
        result.append([each.get_link(), each.get_title()])
    return result
    # return data_handler.get_best_n_match_news(data_handler.rss_all[news_id], n)
server.register_function(get_best_n_match, 'get_best_n_match')

# Server on
debug_tools.console_print("data_server is ready to go")
server.serve_forever()
