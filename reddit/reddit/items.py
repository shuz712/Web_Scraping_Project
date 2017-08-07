# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RedditItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #rank = scrapy.Field()
    link = scrapy.Field()
    title=scrapy.Field()
    submitter = scrapy.Field()
    submitter_link = scrapy.Field()
    source=scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    topic_vote = scrapy.Field()
    percentage_of_upvotes = scrapy.Field()
    num_of_comments = scrapy.Field()
    top_comment = scrapy.Field()
    top_comment_vote = scrapy.Field()
    top_comment_child = scrapy.Field()
    top_comment_username = scrapy.Field()
    subreddit = scrapy.Field()
    user_interests = scrapy.Field()
