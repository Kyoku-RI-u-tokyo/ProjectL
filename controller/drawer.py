# coding:utf-8
from model import rss_handler

livedoor = rss_handler.parse_livedoor()

def main_tab_drawer():
    main_tab = ""
    category = livedoor.keys()

    main_tab += "<ul>\n"
    for i in xrange(len(category)):
        main_tab += """<li><a href="#{index}">{tab_title}</a></li>""".format(index="tabs_"+str(i),
                                                                             tab_title=category[i])
        main_tab += "\n"
    main_tab += "</ul>\n"

    for i in xrange(len(category)):
        content = ""
        for news in livedoor[category[i]]["entries"]:
            title = news["title"].encode("utf8")
            link = news["link"].encode("utf8")
            content += """<a href = "{link}">{text}</a><br>""".format(link=link, text=title)
            content += "\n"

        main_tab += """<div id = "{index}"><p>""".format(index="tabs_"+str(i))
        main_tab += content
        main_tab += "</p></div>"
        main_tab += "\n"

    return main_tab


def news_drawer():
    return ""
