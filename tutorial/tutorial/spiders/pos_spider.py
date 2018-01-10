import scrapy
import string
import re
from scrapy.selector import Selector

regex = re.compile(r'<!--(.*)-->', re.DOTALL)

class PosSpider(scrapy.Spider):
	"""This Spider crawls baseball-reference.com
	and gets player stats and salary info.
	Only looks for batting stats.
	"""

	name = "pos_spider"

	custom_settings = {
		"DOWNLOAD_DELAY": 0,
		"CONCURRENT_REQUESTS_PER_DOMAIN": 3,
		"HTTPCACHE_ENABLED": True,
		}
 
	#start_urls = ['https://www.baseball-reference.com/players/' + z + '/' for z in string.ascii_lowercase]
	start_urls = ['https://www.baseball-reference.com/players/a/']

	def parse(self, response):
		"""
		Parse each "letter page."
		"""
		for href in response.xpath(
			'//div[@id="div_players_"]/p/a/@href'
			).extract():

				url = 'https://www.baseball-reference.com' + href

				yield scrapy.Request(
					url=url,
					callback=self.parse_player,
					meta={'url': url}
					)

	def parse_player(self, response):
		"""
		Scrape a player's page.
		"""

		player_name = (
			(response.xpath('//h1/text()').extract_first()))

		position = (
			response.xpath('//div[@id="meta"]/div[2]/p[1]/text()').extract()[1].strip())


		#### BATTING STATS ####


		for row in response.xpath('//table[@id="batting_standard"]/tbody/tr[@class="full"]'):

			year = row.xpath('./th[@data-stat="year_ID"]/text()').extract_first()

			age = row.xpath('./td[@data-stat="age"]/text()').extract_first()

			team = row.xpath('./td[@data-stat="team_ID"]/a/text()').extract_first()

			hr = row.xpath('./td[@data-stat="HR"]/text()').extract_first()

			rbi = row.xpath('./td[@data-stat="RBI"]/text()').extract_first()

			avg = row.xpath('./td[@data-stat="batting_avg"]/text()').extract_first()

			obp = row.xpath('./td[@data-stat="onbase_perc"]/text()').extract_first()

			slg = row.xpath('./td[@data-stat="slugging_perc"]/text()').extract_first()

			ops = row.xpath('./td[@data-stat="onbase_plus_slugging"]/text()').extract_first()

			# Deal with that godawful commented-out HTML.
			commented_text = response.xpath('//comment()').re(regex)[16]

			new_selector = Selector(text=commented_text, type='html')

			year_row_string = '//tr[@id="batting_value.' + year + '"]'

			year_row = new_selector.xpath(year_row_string)

			war = year_row.xpath('./td[@data-stat="WAR"]/text()').extract_first()

			salary = year_row.xpath('./td[@data-stat="Salary"]/text()').extract_first()

			stats = {
				'player_name': player_name,
				'position': position,
				'year': year,
				'age': age,
				'team': team,
				'hr': hr,
				'rbi': rbi,
				'avg': avg,
				'obp': obp,
				'slg': slg,
				'ops': ops,
				'war': war,
				'salary': salary
				}

			yield stats