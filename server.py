# coding:utf-8

import web
import conf

urls = (
    "/", "Home"
)

app = web.application(urls, globals())

render = web.template.render("view/")


class Home:
    def GET(self):
        return render.home(site_title=conf.site_title, stylesheet=conf.stylesheet, jquery_core=conf.jquery_core,
                           jquery_ui=conf.jquery_ui, tabs_num=conf.tabs_num, t=conf.t)

if __name__ == "__main__":
    app.run()
