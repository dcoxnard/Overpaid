from bs4 import BeautifulSoup
import requests
import re

def get_pitcher_stats(url):
	"""
	This function takes a url as an argument.
	url should be a single pitcher's baseball-reference
	stats sheet page.
	The function return a dictionary of their desired
	stats for all years available.
	"""
	r = requests.get(url).text
	comm = re.compile("<!--|-->")
	cleaned = comm.sub("", r)
	soup = BeautifulSoup(cleaned, 'lxml')

	years = range(2000, 2018)
	data = {}
	for year in years:
		# pitching_standard stats:
		s = ['age', 'team_ID', 'W', 'L', 'G',
			'win_loss_perc', 'earned_run_avg',
			'IP', 'SO', 'strikeouts_per_nine']

		# pitching_value stats:
		v = ['WAR_pitch', 'Salary', 'award_summary']

		output_s = []
		for stat in s:
			t = 'pitching_standard.' + str(year)
			try:
				yd = soup.find(id=t)
				new_stat = yd.find(attrs={'data-stat':stat}).text
			except:
				new_stat = ''
			output_s.append(new_stat)
		data[year] = output_s

		output_v = []
		for stat in v:
			t = 'pitching_value.' + str(year)
			try:
				yd = soup.find(id=t)
				new_stat = yd.find(attrs={'data-stat':stat}).text
			except:
				new_stat = ''
			output_v.append(new_stat)
		data[year] += output_v

	return data

print(get_pitcher_stats('https://www.baseball-reference.com/players/a/aardsda01.shtml'))