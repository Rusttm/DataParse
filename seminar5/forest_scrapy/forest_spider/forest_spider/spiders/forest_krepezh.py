import scrapy


class ForestKrepezhSpider(scrapy.Spider):
    name = "forest_krepezh"
    allowed_domains = ["for-est.ru"]
    start_urls = ["https://for-est.ru/catalog/krepezh/"]

    def parse(self, response):
        pass
