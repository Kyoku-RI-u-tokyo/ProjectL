# coding:utf-8

import time

import web
import drawer

from model import conf

urls = (
    "/", "Home"
)

app = web.application(urls, globals(), autoreload=True)

render = web.template.render("view/", cache=False)


main_tab = drawer.main_tab_drawer()
t = str(time.time())  # 想让这里每次刷新



class Home:
    def GET(self):
        return render.home(site_title=conf.site_title,
                           stylesheet=conf.stylesheet,
                           jquery_core=conf.jquery_core,
                           jquery_ui=conf.jquery_ui,
                           main_tab=main_tab, t=t)

if __name__ == "__main__":
    app.run()
