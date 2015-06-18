# coding:utf-8

import web

from controller import drawer
import conf

urls = (
    "/", "HomeView",
    "/article", "NewsView"
)

app = web.application(urls, globals(), autoreload=True)
render = web.template.render("view/", cache=False)

t = ""
class HomeView:
    def GET(self):
        return render.home(site_title=conf.site_title,
                           jquery_conf=conf.jquery_conf,
                           main_tab=drawer.main_tab_drawer(), t=t)

class NewsView:
    def GET(self):
        form = web.input(news_id="0")
        news_id = form.news_id
        return render.news(news_id=news_id)




if __name__ == "__main__":
    app.run()
