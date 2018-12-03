# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request


class RokomariSpider(Spider):
    name = 'rokomari'
    allowed_domains = ['rokomari.com']
    start_urls = ['http://rokomari.com/book/categories?ref=mm',]
    
    def parse(self, response):
        categories = response.xpath('//div[@class="pFIrstCatCaroItem"]')
        #for every category this loop will scrape urls
        for category in categories:
            url = category.xpath('.//a/@href').extract_first()
            absolute_url = response.urljoin(url)
            #after entering in absolute_url it will enter in parse_listing defination
            yield Request(absolute_url, callback=self.parse_listing)
    def parse_listing(self, response):
        books = response.xpath('//a[@class="btn home-details-btn btn-block"]')
        #for every book this loop will scrape books
        for book in books:
            book_url = book.xpath('.//@href').extract_first()
            absolute_book_url = response.urljoin(book_url)
            #if book_url open then it will redirect to parse_books defination
            yield Request(absolute_book_url, callback=self.parse_books)
        #next page url
        next_page_url = response.xpath('//div[@class="pagination"]/a[last()]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)

        text = response.xpath('//div[@class="pagination"]/a[last()]/text()').extract_first()
        if text == 'Next':
            yield Request(absolute_next_page_url, callback=self.parse_listing)

    def parse_books(self, response):
        book_name = response.xpath('//table[@class="table table-bordered"]/tr[1]/td[2]/text()').extract_first()
        price = response.xpath('//p[@class="details-book-info__content-book-price"]/text()').extract_first()
        writer = response.xpath('//table[@class="table table-bordered"]/tr[2]/td[2]/a/text()').extract_first()
        publisher = response.xpath('//table[@class="table table-bordered"]/tr/td[@class="publisher-link"]/a/text()').extract_first()
        
        yield{"Book Name": book_name,
              "Price": price,
              "Writer": writer,
              "Publisher": publisher}