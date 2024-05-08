import scrapy


class ForestKrepezhSpider(scrapy.Spider):
    name = "forest_krepezh"
    allowed_domains = ["for-est.ru"]
    start_urls = ["https://for-est.ru/catalog/krepezh/"]

    def parse(self, response):
        positions = response.xpath('//div[contains(@class, "item_block")]')
        for pos in positions:
            pos_info = pos.xpath('./div/div[2]/div/div[contains(@class, "item_info")]')
            prod_name = pos_info.xpath('./div[contains(@class, "item-title")]/a/span/text()').get().strip()
            prod_href = pos_info.xpath('./div[contains(@class, "item-title")]/a/@href').get()
            # prod_price_price_kilo = pos_info.xpath('./div[contains(@class,"cost")]/div/div[contains(@class, "price")]/@data-value').get()
            # prod_price_str = pos.xpath('./div/div[2]/div/div[contains(@class, "footer_button")]/div[2]/div[contains(@class, "total_sum")]/div/span/text()').get()
            # prod_price_2 = pos_info.xpath('./div[contains(@class, "cost prices")]/div/div/span/span/text()').get()
            # prod_price = float(prod_price_str.strip().replace(",", "."))
            # print(prod_name, prod_href)
            context = dict({'prod_name': prod_name, 'prod_href': prod_href})
            yield response.follow(url=prod_href, callback=self.parse_prod, meta=context)
        next_page_href = response.xpath('//a[@class="flex-next"]/@href').extract()
        # if next_page_href and next_page_href[0] != '/catalog/krepezh/?PAGEN_1=3':
        if next_page_href:
            next_page_url = response.urljoin(next_page_href[0])
            request = scrapy.Request(url=next_page_url)
            yield request
        else:
            print("end of pages list")

    def parse_prod(self, response):
        prod_card = response.xpath('//div[@class= "page "]')
        prod_name = response.request.meta['prod_name']
        prod_href = response.request.meta['prod_href']
        # prod_name_new = prod_card.xpath('./section/h1/text()').get().strip()
        prod_price_1k = prod_card.xpath('.//span[@class="price_value"]/text()').get().strip()
        prod_box = prod_card.xpath('//div[contains(@class, "counter_block_info")]/@data-countinpack').get().strip()
        try:
            prod_price_1k = prod_price_1k.replace(" ", "")
            prod_price = float(prod_price_1k.replace(",", "."))
        except:
            prod_price = None

        try:
            prod_box = prod_box.replace(" ", "")
            prod_in_box = float(prod_box.replace(",", "."))
        except:
            prod_in_box = 1
        prod_box_price = prod_price * prod_in_box
        prod_descr = prod_card.xpath('//div[contains(@class, "detail_text")]//text()')
        prod_descr_list = [elem.get().strip() for elem in prod_descr]
        prod_description = "\n".join(prod_descr_list)
        prod_stock = prod_card.xpath('//div[contains(@class, "item-stock")]/span[2]/text()').get().strip()
        yield {"prod_name": prod_name, "prod_stock": prod_stock, "prod_price": prod_price, "prod_in_box": prod_in_box,
               "prod_box_price": prod_box_price, "prod_descr": prod_description, 'prod_href': prod_href}
