# coding:utf-8
from supporter import debug_tools


# For Web:
jquery_conf = {
    "stylesheet": "\"http://code.jquery.com/ui/1.11.4/themes/ui-lightness/jquery-ui.css\"",
    "core": "\"http://code.jquery.com/jquery-1.11.3.js\"",
    "ui": "\"http://code.jquery.com/ui/1.11.4/jquery-ui.js\""
    }
    
site_title = "ProjectL" #TODO: set this a better title

news_view_root_url = "/article"

# For Model:
hash_size = 64
word_types_to_retain = ["名詞"]
weight_table = {"名詞固有名詞": 4,      #TODO: 测试一下这个相等方面有没有编码上的问题
                "名詞数": 0,
                "名詞代名詞": 0,
                "名詞接尾": 0}

# For Resources
livedoor_rss = {"主要": "http://news.livedoor.com/topics/rss/top.xml",
                  "国内": "http://news.livedoor.com/topics/rss/dom.xml",
                  "海外": "http://news.livedoor.com/topics/rss/int.xml",
                  "IT 経済": "http://news.livedoor.com/topics/rss/eco.xml",
                  "芸能": "http://news.livedoor.com/topics/rss/ent.xml",
                  "スポーツ": "http://news.livedoor.com/topics/rss/spo.xml",
                  "映画": "http://news.livedoor.com/rss/summary/52.xml",
                  "グルメ": "http://news.livedoor.com/topics/rss/gourmet.xml",
                  "女子": "http://news.livedoor.com/topics/rss/love.xml",
                  "トレンド": "http://news.livedoor.com/topics/rss/trend.xml"}

all_rss = livedoor_rss.values() + ["http://news.goo.ne.jp/rss/topstories/nation/index.rdf"]


          # ["http://headlines.yahoo.co.jp/rss/all-dom.xml",  # ヤフーニュース　国内
          #                          "http://headlines.yahoo.co.jp/rss/all-c_int.xml",  # ヤフーニュース　国際
          #                          "http://headlines.yahoo.co.jp/rss/all-bus.xml",  # ヤフーニュース　経済
          #                          "http://headlines.yahoo.co.jp/rss/all-c_ent.xml",  # ヤフーニュース　エンタメ
          #                          "http://headlines.yahoo.co.jp/rss/all-c_spo.xml",  # ヤフーニュース　スポーツ
          #                          "http://headlines.yahoo.co.jp/rss/all-c_sci.xml",  # ヤフーニュース　IT・科学
          #                          "http://headlines.yahoo.co.jp/rss/all-c_life.xml",  # ヤフーニュース　ライフ
          #                          "http://headlines.yahoo.co.jp/rss/all-loc.xml"]  # ヤフーニュース　地域


if __name__ == "__main__":
    debug_tools.console_print("all_rss:")
    for each in all_rss:
        print("  {each}".format(each=each))



