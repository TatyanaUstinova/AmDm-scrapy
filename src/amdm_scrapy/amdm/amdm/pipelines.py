# -*- coding: utf-8 -*-


import psycopg2

from amdm.items import ArtistItem, SongItem


class PostgresPipeline(object):

    def __init__(self, connection_string):

        self.connection_string = connection_string

        self.artist_id = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(connection_string=crawler.settings.get('POSTGRES_CONNECTION_STRING'))

    def open_spider(self, spider):
        self.conn = psycopg2.connect(self.connection_string)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):

        if isinstance(item, ArtistItem):

            with self.conn.cursor() as cur:

                cur.execute('''
                insert into artists("name") 
                    values(%s)
                    returning id;''', [
                    item['name']
                ])

                self.artist_id = cur.fetchone()[0]

            self.conn.commit()

            return item

        if isinstance(item, SongItem):

            with self.conn.cursor() as cur:

                item['artist_id'] = self.artist_id

                cur.execute('''
                insert into songs(artist_id, "name", "text")
                    values(%s, %s, %s);''', [
                    item['artist_id'], item['name'], item['text']
                ])

                self.conn.commit()

                return item
