# coding:utf-8

import time

import web
import drawer

from model import conf

urls = (
    "/", "HomeView",
    "/article", "NewsView"
)

app = web.application(urls, globals(), autoreload=True)

render = web.template.render("view/", cache=False)



main_tab = drawer.main_tab_drawer()
t = None
class HomeView:
    def GET(self):
        return render.home(site_title=conf.site_title,
                           stylesheet=conf.stylesheet,
                           jquery_core=conf.jquery_core,
                           jquery_ui=conf.jquery_ui,
                           main_tab=main_tab, t=t)



class NewsView:
    def GET(self):
        form = web.input(news_id="0")
        news_id = form.news_id
        return render.news(news_id=news_id)




if __name__ == "__main__":
    app.run()
