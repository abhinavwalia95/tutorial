# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
from tutorial.items import blos_categ_Item,blos_list_categ_Item
from scrapy_splash import SplashRequest

class BookListOnlineSpider(scrapy.Spider):
    name = "blos"
    allowed_domains = ["http://booklistonline.com/"]
    start_urls = [
        "http://booklistonline.com/Book-Reviews.aspx?AspxAutoDetectCookieSupport=1"
    ]
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,endpoint='render.html',args= {'wait': 0.5})

    def parse(self, response):
        for sel in response.xpath('//div[@class="TaxonomyItem"]/h3/a[@class="TaxonomyItemLev1"]'):
            item=blos_categ_Item()
            item['categ_name']=sel.xpath('text()').extract()
            item['categ_link']=sel.xpath('@href').extract()
            yield item
            yield scrapy.Request(response.urljoin(item['categ_link']), callback=self.parse_categ_contents)

    def parse_categ_contents(self, response):
        for sel in response.xpath('//table/tbody/tr/td/table/tbody/tr/td[@class="styleSRBibD"]'):
            item=blos_list_categ_Item()
            item['categ_item_name']=sel.xpath('span[@class="style22"]/a/strong/text()').extract()
            item['categ_item_author']=sel.xpath('font/b/text()').extract()
            yield item
        next_page=response.xpath('//a[@id="ctl00_CentralContentPlaceHolder_lnkNextPage"]/@href')
        if next_page:
            url=response.urljoin(next_page[0].extract())
            yield scrapy.Request(url,self.parse_categ_contents)
