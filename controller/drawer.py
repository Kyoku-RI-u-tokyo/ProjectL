# coding:utf-8
from supporter import debug_tools
import conf
import xmlrpclib
server = xmlrpclib.ServerProxy('http://localhost:10000')

def main_tab_drawer():
    to_draw = ""
    livedoor = server.get_livedoor()
    category = livedoor.keys()

    to_draw += "<ul>\n"
    for i in xrange(len(category)):
        to_draw += """<li><a href="#{index}">{tab_title}</a></li>""".format(index="tabs_" + str(i),
                                                                            tab_title=category[i].encode("utf8"))
        to_draw += "\n"
    to_draw += "</ul>\n"

    for i in xrange(len(category)):
        content = ""
        for news in livedoor[category[i]]:
            title = news[0].encode("utf8")
            link = news[1].encode("utf8")
            content += """<a href = "{link}">{text}</a><br>""".format(link=link, text=title)
            content += "\n"

        to_draw += """<div id = "{index}"><p>""".format(index="tabs_" + str(i))
        to_draw += content
        to_draw += "</p></div>"
        to_draw += "\n"

    return to_draw

def best_match_drawer(news_id):
    # debug_tools.console_print(str(news_id))
    bests = server.get_best_n_match(news_id)
    to_draw = ""
    for each in bests:
        title = each[1].encode("utf8")
        link = conf.news_view_root_url + "?news_id=" + each[0].encode("utf8") \
               + "&" + "title=" + title

        to_draw += """<a href = "{link}">{text}</a><br>""".format(link=link, text=title)


    return to_draw
