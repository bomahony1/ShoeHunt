import scrapy
from scraper.items import JDSportItem

class JdsportSpider(scrapy.Spider):
    custom_settings = {
    'ITEM_PIPELINES': {
      'scraper.pipelines.SavingToPostgresPipeline2': 400
        }
    }

    name = "jdsportspider"
    allowed_domains = ["jdsports.ie"]
    start_urls = ["https://www.jdsports.ie/men/mens-footwear/sale/"]

    def parse(self, response):
        shoes = response.css("span.itemContainer")

        for shoe in shoes:
            # Extracting the relative URL
            relative_url = shoe.css('span a::attr(href)').get()

            # Converting the relative URL to an absolute URL
            absolute_url = response.urljoin(relative_url)
            self.log(f"Absolute URL: {absolute_url}")
            print(absolute_url)

            # Yielding the absolute URL
            yield response.follow(absolute_url, callback=self.parse_shoe)

    def parse_shoe(self, response):
        item = JDSportItem ({
            'title': response.css("#productItemTitle h1::text").get(),
            'category': response.css('#itemRelatedCats a::text').get(),
            'original_price': response.css("span.was span::text").get(),
            'discount_price': response.css("span.now span::text").get(),
            'discount_percent': response.css('.sav::text').get(),
            'image_url': response.css('li.tap-zoom img::attr(src)').get(),
            'description': response.css('#itemInfoContainer div::text').get(),
            'product_url': response.url 
        })
        
        yield item