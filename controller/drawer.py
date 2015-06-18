# coding:utf-8
import xmlrpclib
server = xmlrpclib.ServerProxy('http://localhost:10000')

def main_tab_drawer():
    main_tab = ""
    livedoor = server.get_livedoor()
    category = livedoor.keys()

    main_tab += "<ul>\n"
    for i in xrange(len(category)):
        main_tab += """<li><a href="#{index}">{tab_title}</a></li>""".format(index="tabs_"+str(i),
                                                                             tab_title=category[i].encode("utf8"))
        main_tab += "\n"
    main_tab += "</ul>\n"

    for i in xrange(len(category)):
        content = ""
        for news in livedoor[category[i]]:
            title = news[0].encode("utf8")
            link = news[1].encode("utf8")
            content += """<a href = "{link}">{text}</a><br>""".format(link=link, text=title)
            content += "\n"

        main_tab += """<div id = "{index}"><p>""".format(index="tabs_"+str(i))
        main_tab += content
        main_tab += "</p></div>"
        main_tab += "\n"

    return main_tab

def news_drawer():
    return ""
