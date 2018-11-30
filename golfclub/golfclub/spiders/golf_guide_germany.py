# -*- coding: utf-8 -*-
import scrapy


class GolfGuideGermanySpider(scrapy.Spider):
    name = 'golf-guide-germany'
    allowed_domains = ['1golf.eu']
    start_urls = ['http://1golf.eu/en/golf-courses/germany/']

    def parse(self, response):
        listings = response.xpath('//h4[@class="item-box__title"]')

        for listing in listings:
            name = listing.xpath('.//a[@class="item-box__title-text"]/text()').extract_first()
            link = listing.xpath('.//a[@class="item-box__title-text"]/@href').extract_first()
            absolute_link = response.urljoin(link)
            yield scrapy.Request(absolute_link, callback=self.parse_listing, 
                                meta={'name': name})

        next_page_url = response.xpath('//a[@class="link-button pagination__button pagination__button--next link-button--small link-button--light"]/@href').extract_first()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

    def parse_listing(self, response):
        club_name = response.meta['name']
        club_address = response.xpath('//p[@class="address-view__addr adr"]/text()').extract_first()
        club_number = response.xpath('//span[@class="tel"]/text()').extract_first()
        club_email = response.xpath('//a[@class="email"]/text()').extract_first()
        yield {'Club name': club_name,
               'Club Address': club_address,
               'Club Number': club_number,
               'Club E-mail': club_email}                
