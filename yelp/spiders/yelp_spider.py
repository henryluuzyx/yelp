import scrapy

class YelpSpider(scrapy.Spider):
    name = 'yelp'
    # allowed_domains = ['https://www.yelp.com']
    start_urls = ['https://www.yelp.com/search?find_loc=Santa+Clara,+CA&start=0&cflt=restaurants']

    def parse(self, response):
    	next_page = scrapy.Selector(response).xpath('//*[@id="super-container"]//a[@class="u-decoration-none next pagination-links_anchor"]/@href').extract_first()
    	print 'https://www.yelp.com' + next_page
    	yield scrapy.Request('https://www.yelp.com' + next_page, callback=self.parse_next)

        # follow pagination links
        child_page = scrapy.Selector(response).xpath('//*[@id="super-container"]//a[@class="biz-name js-analytics-click"]/@href').extract()
        for i in child_page:
        	if "/biz/" in i:

        		print 'https://www.yelp.com' + i
        		yield scrapy.Request('https://www.yelp.com'+i, callback=self.parse_data)
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     print next_page
            # yield scrapy.Request(next_page, callback=self.parse)

    def parse_next(self, response):
    	next_page = scrapy.Selector(response).xpath('//*[@id="super-container"]//a[@class="u-decoration-none next pagination-links_anchor"]/@href').extract_first()

    	print 'https://www.yelp.com' + next_page
    	yield scrapy.Request('https://www.yelp.com' + next_page, callback=self.parse)

    def parse_data(self, response):
        def extract_data(data):
            tmp = scrapy.Selector(response).xpath(data).extract_first()
            if not tmp:
                return ''
            return tmp.strip()

        def extract_address_full(data):
            tmp = scrapy.Selector(response).xpath(data).extract()
            temp = ""
            for i in tmp:
                temp = temp + i + ", "
            return temp[:-2].strip()

        def extract_address(data, i):
            tmp = scrapy.Selector(response).xpath(data).extract()
            return tmp[i].strip()
        yield {
            'url': response.url,
            'address': extract_address('//*[@class="street-address"]//address/text()', 0),
            'county': extract_address('//*[@class="street-address"]//address/text()', 1),
            'address_full': extract_address_full('//*[@class="street-address"]//address/text()'),
            'mobile': extract_data('//*[@class="biz-phone"]/text()'),
            'website': extract_data('//*[@class="biz-website js-add-url-tagging"]//a/text()'),
            'name': extract_data('//*[@class="biz-page-title embossed-text-white shortenough"]/text()'),
            'name_full': extract_data('//*[@class="biz-page-header-left claim-status"]//h1/text()'),
        }