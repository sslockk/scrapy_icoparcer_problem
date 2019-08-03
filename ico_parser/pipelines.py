# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

CLIENT = MongoClient('localhost', 27017)
MONGO_DB = CLIENT.ico
COLLECTION = MONGO_DB.icobench


class IcoParserPipeline(object):
    project_collection = MONGO_DB.icobench
    people_collection = MONGO_DB.people

    def people_create_of_update(self, people_item):
        db_item = self.people_collection.find_one({'source_page_url': people_item.get('source_page_url')})
        if db_item:
            people_item['_id'] = db_item.get('_id')
        else:
            self.people_collection.insert_one(people_item)

    def process_item(self, item, spider):

        if item.get('team'):
            _ = [self.people_create_of_update(itm.get('person')) for itm in item.get('team')]
            item['team'] = [
                {'person': itm.get('person').get('_id'),
                 'position': itm.get('position')
                 } for itm in item['team']]

        if item.get('advisors'):
            _ = [self.people_create_of_update(itm.get('person')) for itm in item.get('advisors')]
            item['advisors'] = [
                {'person': itm.get('person').get('_id'),
                 'position': itm.get('position')
                 } for itm in item['advisors']]

        _ = self.project_collection.insert_one(item)

        return item
