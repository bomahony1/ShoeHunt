# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from urllib.parse import urlparse, urlunparse
import psycopg2
from scrapy.exceptions import DropItem
import os
from dotenv import load_dotenv




class ScraperPipeline:
    def process_item(self, item, spider):
        # Extracting the 'price' field from the item
        price = item.get('price')

        # Check if 'price' is not None before trying to replace the character
        if price is not None:
            # Replace "£" character with an empty string
            price = price.replace("£", "")

        return item


class SavingToPostgresPipeline(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = psycopg2.connect(
            host= os.getenv('HOST'),
            port= os.getenv('PORT'),
            user= os.getenv('DBUSER'),
            password= os.getenv('DBPASSWORD'),
            database= os.getenv('DATABASE')
        )
        self.curr = self.conn.cursor()

        drop_table_sql = "DROP TABLE IF EXISTS nike"
        self.curr.execute(drop_table_sql)

        sql = """
        CREATE TABLE IF NOT EXISTS nike (
            title VARCHAR(256),
            description VARCHAR(512),
            category VARCHAR(256),
            original_price VARCHAR(256),
            discount_price VARCHAR(256),
            image_url VARCHAR(256)
        )
        """
        try:
            self.curr.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(f"Error creating table: {e}")

    def process_item(self, item, spider):
        query = """
        INSERT INTO nike (title, category, original_price, discount_price, image_url, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        data = (
            item["title"],
            item["category"],
            item["original_price"],
            item["discount_price"],
            item["image_url"],
            item["description"],
        )
        try:
            self.curr.execute(query, data)
            self.conn.commit()
            print("Successful")
            return item
        except Exception as e:
            print(f"Error storing item in the database: {e}")

        return item
    
    def close_spider(self, spider):
        self.curr.close()
        self.conn.close()


class ModifyImageUrlPipeline:
    def process_item(self, item, spider):
        # Replace "t_PDP_LOADING_v1" with "t_PDP_1728_v1" in the image URL
        item["image_url"] = item["image_url"].replace("t_PDP_LOADING_v1", "t_PDP_1728_v1")

        return item




