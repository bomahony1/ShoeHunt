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


class ScraperPipeline:
    def process_item(self, item, spider):
        # Extracting the 'price' field from the item
        price = item.get('price')

        # Check if 'price' is not None before trying to replace the character
        if price is not None:
            # Replace "£" character with an empty string
            price = price.replace("£", "")


import os
import psycopg2

class SavingToPostgresPipeline(object):
    def __init__(self, table_name):
        self.table_name = table_name
        self.create_connection()

    def create_connection(self):
        self.conn = psycopg2.connect(
            host=os.getenv('HOSTL'),
            port=os.getenv('PORTL'),
            user=os.getenv('DBUSERL'),
            password=os.getenv('DBPASSWORDL'),
            database=os.getenv('DATABASEL')
        )
        self.curr = self.conn.cursor()

        drop_table_sql = f"DROP TABLE IF EXISTS {self.table_name}"
        self.curr.execute(drop_table_sql)

        id_start_value = 0

        if self.table_name == 'nike':
            id_start_value = 1
        elif self.table_name == 'jdsport':
            id_start_value = 101


        sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            title VARCHAR(256),
            category VARCHAR(256),
            original_price VARCHAR(256),
            discount_price VARCHAR(256),
            discount_percent VARCHAR(256),
            image_url VARCHAR(552),
            description TEXT,
            product_url VARCHAR(552),
            logo VARCHAR(552),
            CONSTRAINT unique_id UNIQUE (id)
        )
        """
        try:
            self.curr.execute(sql)
            # Set the custom starting value
            self.curr.execute(f"ALTER SEQUENCE {self.table_name}_id_seq RESTART WITH {id_start_value}")
            self.conn.commit()
        except Exception as e:
            print(f"Error creating table: {e}")

    def process_item(self, item, spider):
        # Conditionally set 'logo' based on the table name
        if self.table_name == 'nike':
            item['logo'] = 'https://i.pinimg.com/564x/33/e6/3d/33e63d5adb0da6b303a83901c8e8463a.jpg'
        elif self.table_name == 'jdsport':
            item['logo'] = 'https://www.logo.wine/a/logo/JD_Sports/JD_Sports-Logo.wine.svg'
        else:
            item['logo'] = None

        # Include 'logo' in the INSERT INTO query dynamically
        query = f"""
        INSERT INTO {self.table_name} (title, category, original_price, discount_price, discount_percent, image_url, description, product_url, logo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (
            item["title"],
            item["category"],
            item["original_price"],
            item["discount_price"],
            item["discount_percent"],
            item["image_url"],
            item["description"],
            item["product_url"],
            item["logo"]
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



class SavingToNikePostgresPipeline(SavingToPostgresPipeline):
    def __init__(self):
        super().__init__("nike")

class SavingToJdSportPostgresPipeline(SavingToPostgresPipeline):
    def __init__(self):
        super().__init__("jdsport")


class ModifyImageUrlPipeline:
    def process_item(self, item, spider):
        # Replace "t_PDP_LOADING_v1" with "t_PDP_1728_v1" in the image URL
        item["image_url"] = item["image_url"].replace("t_PDP_LOADING_v1", "t_PDP_1728_v1")
        # Replace "w=750&h=531" with "width="305" height="350""
    
        return item

# scraper/scraper/pipelines.py

from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

class ModifyImgURLPipeline:
    def process_item(self, item, spider):
        if 'image_url' in item:
            item['image_url'] = self.modify_url(item['image_url'])
        return item

    def modify_url(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        # Modify the width and height parameters
        query_params['w'] = ['305']
        query_params['h'] = ['350']

        # Update the query string
        parsed_url = parsed_url._replace(query=urlencode(query_params, doseq=True))
        modified_url = parsed_url._replace(query=urlencode(query_params, doseq=True))

        return urlunparse(modified_url)




