# -*- coding: utf-8 -*-


import scrapy


class ArtistItem(scrapy.Item):
    name = scrapy.Field()


class SongItem(scrapy.Item):
    artist_id = scrapy.Field()
    name = scrapy.Field()
    text = scrapy.Field()
