# coding:utf-8

import feedparser
import content_handler
import conf

class News():
    def __init__(self, title, link):
        self.news_title = title
        self.news_link = link
        self.news_id = self.news_link
        self.news_simhash_value = self.__cal_simhash_value()

    def __cal_simhash_value(self):
        return content_handler.cal_simhash(self.news_title)

    def get_title(self):
        return self.news_title

    def get_link(self):
        return self.news_link

    def get_id(self):
        return self.news_id

    def get_simhash_value(self):
        return self.news_simhash_value

    def display_simhash_value_bin(self):
        print(bin(self.news_simhash_value))

    def __str__(self):
        return "Object of [News]: title: {title}, link: {link}, id: {id}, simhash_value: {simhash_value}".format(title=self.news_title,
                                                                                                                 link=self.news_link,
                                                                                                                 id=self.news_id,
                                                                                                                 simhash_value=self.news_simhash_value)

def parse_livedoor():
    parsed_livedoor_rss = {}
    for each_key in conf.livedoor_rss.keys():
        parsed_livedoor_rss[each_key] = feedparser.parse(conf.livedoor_rss[each_key])

    return parsed_livedoor_rss

def parse_all():
    """parse all the RSS resources"""
    resources = []
    for each_rss_xml in conf.all_rss:
        parsed = feedparser.parse(each_rss_xml)
        for each in parsed["entries"]:
            news = News(each["title"].encode("utf8"), each["link"].encode("utf8"))
            resources.append(news)

    return resources
