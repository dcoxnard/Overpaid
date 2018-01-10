import scrapy
import string
import re
from scrapy.selector import Selector

regex = re.compile(r'<!--(.*)-->', re.DOTALL)

class PitcherSpider(scrapy.Spider):
	"""This Spider crawls baseball-reference.com
	and gets player stats and salary info.
	Only looks for pitching stats.
	"""

	name = "pitcher_spider2"

	custom_settings = {
		"DOWNLOAD_DELAY": 0,
		"CONCURRENT_REQUESTS_PER_DOMAIN": 3,
		"HTTPCACHE_ENABLED": True,
		}
 
	start_urls = ['https://www.baseball-reference.com/players/' + z + '/' for z in string.ascii_lowercase]
	#start_urls = ['https://www.baseball-reference.com/players/a/']

	def parse(self, response):
		"""
		Parse each "letter page."
		"""
		
		player_div = response.xpath('//div[@id="div_players_"]')
		for p in player_div.xpath('./p'):
		    active = p.xpath('./text()').extract_first()
		    player = p.xpath('./a/text()').extract_first()
		    href = p.xpath('./a/@href').extract_first()
		    if not player:
		         active = p.xpath('./b/text()').extract_first()
		         player = p.xpath('./b/a/text()').extract_first()
		         href = p.xpath('./b/a/@href').extract_first()
		    url = 'https://www.baseball-reference.com' + href
		    if '20' in active:
		    	yield scrapy.Request(
					url=url,
					callback=self.parse_player)


	def parse_player(self, response):
		"""
		Scrape a player's page.
		"""

		player_name = (
			(response.xpath('//h1/text()').extract_first()))

		position = (
			response.xpath('//div[@id="meta"]/div[2]/p[1]/text()').extract()[1].strip())


		#### PITCHING STATS ####


		for row in response.xpath('//table[@id="pitching_standard"]/tbody/tr[@class="full"]'):

			year = row.xpath('./th[@data-stat="year_ID"]/text()').extract_first()

			age = row.xpath('./td[@data-stat="age"]/text()').extract_first()

			team = row.xpath('./td[@data-stat="team_ID"]/a/text()').extract_first()

			wins = row.xpath('./td[@data-stat="W"]/text()').extract_first()

			losses = row.xpath('./td[@data-stat="L"]/text()').extract_first()

			win_loss_perc = row.xpath('./td[@data-stat="win_loss_perc"]/text()').extract_first()

			era = row.xpath('./td[@data-stat="earned_run_avg"]/text()').extract_first()

			g = row.xpath('./td[@data-stat="G"]/text()').extract_first()

			ip = row.xpath('./td[@data-stat="IP"]/text()').extract_first()

			so = row.xpath('./td[@data-stat="SO"]/text()').extract_first()

			so9 = row.xpath('./td[@data-stat="strikeouts_per_nine"]/text()').extract_first()

			# Deal with that godawful commented-out HTML.
			commented_text = response.xpath('//comment()').re(regex)[16]

			new_selector = Selector(text=commented_text, type='html')

			year_row_string = '//tr[@id="pitching_value.' + year + '"]'

			year_row = new_selector.xpath(year_row_string)

			war = year_row.xpath('./td[@data-stat="WAR_pitch"]/text()').extract_first()

			salary = year_row.xpath('./td[@data-stat="Salary"]/text()').extract_first()

			stats = {
				'player_name': player_name,
				'position': position,
				'year': year,
				'age': age,
				'team': team,
				'wins': wins,
				'losses': losses,
				'win_loss_perc': win_loss_perc,
				'era': era,
				'g': g,
				'ip': ip,
				'so': so,
				'so9': so9,
				'war': war,
				'salary': salary
				}

			yield stats