# scrapy crawl amdm -a sign="milky chance"

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector

from amdm.items import ArtistItem, SongItem


class AmDmSpider(scrapy.Spider):

    name = 'amdm'

    def __init__(self, sign, *args, **kwargs):
        super(AmDmSpider, self).__init__(*args, **kwargs)

        self.start_urls = [
            'https://amdm.ru/search/?q={}'.format(sign),
        ]

    def parse(self, response):
        """
        'https://amdm.ru/search/?q=milky chance' -> 'https://amdm.ru/akkordi/milky_chance/'
        Parses the search result page for artist page URL grabbing and following to it.
        :param response:
        :return:
        """

        table = response.xpath('//table[@class="items"]/tr')[1]
        rows = table.xpath('//a[@class="artist"]')
        href = rows.css('a::attr("href")').extract_first()
        artist_url = 'https:{}'.format(href)

        yield response.follow(artist_url, self.parse_artist)

    def parse_artist(self, response):
        """
        'https://amdm.ru/akkordi/milky_chance/' -> 'https://amdm.ru/akkordi/milky_chance/157186/flashed_junk_mind/'
        Parses the artist page for artist's name and songs page URL grabbing and following to them.
        Creates ArtistItem instance.
        :param response:
        :return:
        """

        artist_name = response.xpath('//h1/text()').extract_first()
        item = ArtistItem(name=artist_name)

        yield item

        for tr in response.xpath('//table[@id="tablesort"]/tr'):
            href = tr.css('a::attr("href")').extract_first()
            song_url = 'https:{}'.format(href)

            yield response.follow(song_url, self.parse_song)

    def parse_song(self, response):
        """
        Parses the song page for song's name and text grabbing.
        Creates the SongItem instance for each song.
        :param response:
        :return:
        """

        song_name = response.xpath('//h1/span[@itemprop="name"]/text()').extract_first()

        text = response.xpath('//pre[@itemprop="chordsBlock"]').extract_first()
        selector = Selector(text=text)

        text_content = selector.xpath("//text()").extract()
        chords = ' '.join(text_content)

        item = SongItem(name=song_name, text=chords)

        yield item
