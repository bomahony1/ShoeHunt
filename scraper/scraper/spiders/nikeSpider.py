import scrapy
import random
from scraper.items import BookItem


class NikeSpider(scrapy.Spider):
    name = "nikespider"
    allowed_domains = ["https://www.nike.com/ie"]
    start_urls = ["https://www.nike.com/ie/w/mens-sale-shoes-3yaepznik1zy7ok"]

    def parse(self, response):
        books = response.css("product-grid__items css-hvew4t")

        for book in books:
            book_link = book.css("h3 a::attr(href)").get() 
            if book_link is not None:
                if 'catalogue/' in book_link:
                    book_url = 'https://books.toscrape.com/' + book_link
                else:
                    book_url = 'https://books.toscrape.com/catalogue/' + book_link
                
            yield response.follow(book_url, callback=self.parse_book_page)

        next_page = response.css('li.next a ::attr(href)').get()

        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback= self.parse)
            

                 
    
    def parse_book_page(self, response):
         
        table_rows = response.css("table tr")
        book_item = BookItem()

     
        book_item['url'] = response.url,
        book_item['title']=  response.css('.product_main h1::text').get(),
        book_item['description']=  response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        book_item['product_type']=  table_rows[1].css('td ::text').get(),
        book_item['price']=  table_rows[2].css('td ::text').get(),
        book_item['availability']=  table_rows[5].css('td ::text').get(),
        book_item['stars']=  response.css("p.star-rating").attrib['class'],
         
        yield book_item
        

        


