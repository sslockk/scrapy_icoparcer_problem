# -*- coding: utf-8 -*-
import scrapy
from ico_parser.items import IcoParserItem, PersonItem
from time import sleep


class IcobenchSpider(scrapy.Spider):
    name = 'icobench'
    allowed_domains = ['icobench.com']
    start_urls = ['https://icobench.com/icos?filterSort=name-asc']


    def ico_page_parse(self, response):
        sleep(0.5)
        data_person = response.css('div#team.tab_content div.row')
        print("data_person", data_person)
        print('-' * 10)
        try:
            team = [
                {
                    'person': PersonItem(
                        person_url=itm.css('a::attr(href)').get(),
                        name=itm.css('h3::text').get(),
                        social_links=itm.css('div.socials a::attr(href)').extract()),
                    'position': itm.css('h4::text').get()
                }
                for itm in data_person[0].css('div.col_3')
            ]


        except IndexError as e:
            print(e)
            team = []

        try:
            advisors = [
                {
                    'person': PersonItem(
                        person_url=itm.css('a::attr(href)').get(),
                        name=itm.css('h3::text').get(),
                        social_links=itm.css('div.socials a::attr(href)').extract()),
                    'position': itm.css('h4::text').get()
                }
                for itm in data_person[1].css('div.col_3')
            ]


        except IndexError as e:
            print(e)
            advisors = []

        data = {'name': response.css('div.ico_information div.name h1::text').get(),
                'slogan': response.css('div.ico_information div.name h2::text').get(),
                'description': response.css('div.ico_information p::text').get(),
                'team': team,
                'advisors': advisors,
                }

        print("data", data)
        item = IcoParserItem(**data)

        yield item

    def parse(self, response):

        next_page = response.css('div.ico_list div.pages a.next::attr(href)').get()
        ico_pages = response.css('div.ico_list td.ico_data div.content a.name::attr(href)').extract()

        print(ico_pages)

        for page in ico_pages:
            sleep(1)
            print(page)
            print('*' * 30)
            yield response.follow(page, callback=self.ico_page_parse)
            

        yield response.follow(next_page, callback=self.parse)

        print(next_page)
