import scrapy
import os
import time

class UnsplashFotoSpider(scrapy.Spider):
    name = "unsplash_foto"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/"]

    def parse(self, response):
        """ parsing list of theme pages on main page"""
        pages_list = response.xpath('//a[@class="oaSYM ZR5jm"]')

        for page in pages_list:
            page_href = page.xpath('./@href').get()
            time.sleep(1)
            page_theme = page.xpath('.//div/text()').get()
            # print(f"{page_theme=}")
            if not page_theme:
                page_theme = page.xpath('./text()').get()
                # print(f"{page_theme=}")
            context = dict({'page_theme': page_theme})
            yield response.follow(url=page_href, callback=self.parse_page, meta=context)
            # break

    def parse_page(self, response):
        """ parses theme page """
        foto_list = response.xpath('//a[@itemprop="contentUrl"]')
        page_theme = response.meta.get('page_theme')
        for foto in foto_list:
            foto_page_href = foto.xpath('./@href').get()
            context = {'foto_page_href': foto_page_href, 'page_theme': page_theme}
            yield response.follow(url=foto_page_href, callback=self.parse_foto, meta=context)
            # break

    def parse_foto(self, response):
        """ parse foto page and extract location"""
        # foto_place = response.xpath('//span[contains(@class,"jU5nt GcCli wP5Cw FEdrY")]/text()').get().strip()
        foto_title = response.xpath('//div[contains(@class, "c489k")]/h1/text()').get().strip()
        foto_img_url = response.xpath('//div[@class="WxXog"]/img/@src').get().strip()
        # foto_img_hrefs_text = response.xpath('//div[@class="WxXog"]/img/@srcset').get()
        # foto_img_hrefs_list = foto_img_hrefs_text.split(",")
        page_theme = response.meta.get("page_theme")
        # foto_img_urls = [href.strip().split(" ") for href in foto_img_hrefs_list]
        # foto_img_urls = foto_img_hrefs_text
        # foto_page_href = response.meta.get("foto_page_href")
        foto_site_name = foto_img_url.split("/")[-1].split("?")[0]
        # yield {'foto_title': foto_title, 'foto_place': foto_place, 'foto_page_href': foto_page_href, 'foto_img_url': foto_img_url, 'foto_img_urls': foto_img_urls}
        file_name = f"{foto_site_name}.jpg"
        up_up_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        image_path = os.path.join(up_up_dir, "images", file_name)
        context = dict({'image_path': image_path})
        yield {"название": foto_title, "категория": page_theme, "ссылка": foto_img_url, "файл": file_name, "путь_к_файлу": image_path}
        yield scrapy.Request(url=foto_img_url, callback=self.save_foto, meta=context)

    def save_foto(self, response):
        image_path = response.meta.get('image_path')
        with open(image_path, "wb") as f:
            f.write(response.body)

