import scrapy
from scraper.items import NikeItem


class NikeSpider(scrapy.Spider):
    custom_settings = {
    'ITEM_PIPELINES': {
        'scraper.pipelines.SavingToPostgresPipeline': 400,
        'scraper.pipelines.ModifyImageUrlPipeline': 200
        }
    }
        
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
        item = NikeItem({
            'title': response.css(".css-1ou6bb2 h1::text").get(),
            'category': response.css(".css-1ou6bb2 h2::text").get(),
            'original_price': response.css(".css-tpaepq::text").get(),
            'discount_price': response.css(".css-xq7tty::text").get(),
            'discount_percent': response.css('.css-14jqfub::text').get(),
            'image_url': response.css('#pdp-6-up img::attr(src)').get(),
            'description': response.css("div.pt6-sm.prl6-sm.prl0-lg div.description-preview.body-2.css-1pbvugb p::text").get(),
            'product_url': response.url 
        })

        yield item