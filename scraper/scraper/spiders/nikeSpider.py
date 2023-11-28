import scrapy
import random
from scraper.items import BookItem



class NikeSpider(scrapy.Spider):
    name = "nikespider"
    allowed_domains = ["nike.com"]
    start_urls = ["https://www.nike.com/ie/w/mens-sale-shoes-3yaepznik1zy7ok"]

    def parse(self, response):
        shoes = response.css("div.product-card__body")

        for shoe in shoes:
            # Extracting the relative URL
            relative_url = shoe.css("figure a::attr(href)").get()

            # Converting the relative URL to an absolute URL
            absolute_url = response.urljoin(relative_url)

            # Yielding the absolute URL
            yield response.follow(absolute_url, callback=self.parse_shoe)

    def parse_shoe(self, response):
        yield {
            'title': response.css(".css-1ou6bb2 h1::text").get(),
            'category': response.css(".css-1ou6bb2 h2::text").get(),
            'original_price': response.css(".css-tpaepq::text").get(),
            'discount_price': response.css(".css-xq7tty::text").get(),
            'image_url': response.css('#pdp-6-up img::attr(src)').get(),
            'description': response.css("div.pt6-sm.prl6-sm.prl0-lg div.description-preview.body-2.css-1pbvugb p::text").get()
        }


           
        

      
            

                 
    
        

        


#  product_name = card.css("div.product-card__title::text").get()
#             product_description = card.css("div.product-card__subtitle::text").get()
#             img_src = card.css('div.wall-image-loader img::attr(src)').get()
#             original_price = card.css("div.product-price.ie__styling::text").get()
#             discount_price = card.css("div.product-price.is--current-price::text").get()

#  yield {
#                 "name": product_name,
#                 "description": product_description,
#                 "img-src": img_src,
#                 "original_price": original_price,
#                 "discount_price": discount_price,
#             