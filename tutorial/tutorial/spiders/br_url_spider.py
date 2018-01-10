import scrapy
import string

class PlayerUrlSpider(scrapy.Spider):
	"""
	This class uses a scrapy Spider to get all the player-urls
	from baseball-reference.com that started playing 
	on or after the year 2000.
	"""

	name = 'br_url_spider'

	custom_settings = {
		"DOWNLOAD_DELAY": 3,
		"CONCURRENT_REQUESTS_PER_DOMAIN": 3,
		"HTTPCACHE_ENABLED": True,
		}

	start_urls = ['https://www.baseball-reference.com/players/' + z + '/' for z in string.ascii_lowercase]

	def parse(self, response):

		for player in response.xpath(
			'//div[@id="div_players_"]/p'):

			href = player.xpath('./a/@href').extract_first()
			if not href:
				href = player.xpath('./b/a/@href').extract_first()

				yrs = player.xpath('./b/text()').extract_first()
			else:
				yrs = player.xpath('./text()').extract_first()

			url = 'https://www.baseball-reference.com' + href
			
			if ('18' not in yrs) and ('19' not in yrs):

				yield {
					'url':url,
					}