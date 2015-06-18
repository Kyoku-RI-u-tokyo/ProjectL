# coding:utf-8

import feedparser

import conf

def parse_livedoor():
    parsed_livedoor_rss = {}
    for each_key in conf.livedoor_rss.keys():
        parsed_livedoor_rss[each_key] = feedparser.parse(conf.livedoor_rss[each_key])

    return parsed_livedoor_rss