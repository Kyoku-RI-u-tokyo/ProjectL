# coding:utf-8
import web
import xmlrpclib
server = xmlrpclib.ServerProxy('http://localhost:10000')

from supporter import debug_tools

def demo_func():
    return server.demo()

from controller import drawer
import conf

urls = (
    "/", "HomeView",
    conf.news_view_root_url, "NewsView"
)

app = web.application(urls, globals(), autoreload=True)
render = web.template.render("view/", globals={'demo_f':demo_func}, cache=False)

t = ""
class HomeView:
    def GET(self):
        return render.home(site_title=conf.site_title,
                           jquery_conf=conf.jquery_conf,
                           main_tab=drawer.main_tab_drawer(), demo_func=demo_func, t=t)

class NewsView:
    def GET(self):
        form = web.input(news_id="", title="")
        news_id = form.news_id
        title = form.title
        return render.news(news_id=news_id, title=title)

if __name__ == "__main__":
    debug_tools.console_print("web_server is ready to go")
    app.run()
