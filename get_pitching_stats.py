from bs4 import BeautifulSoup
import requests
import re

# This file gets age for David Aardsma.
url_aards = 'https://www.baseball-reference.com/players/a/aardsda01.shtml'
r = requests.get(url_aards).text
comm = re.compile("<!--|-->")
cleaned = comm.sub("", r)
soup = BeautifulSoup(cleaned, 'lxml')

years = range(2000, 2018)
data = {}
for year in years:
	#t = 'pitching_value.' + str(year)
	#try:
	#	yd = soup.find(id=t)
	#	war = yd.find(attrs={'data-stat':'WAR_pitch'}).text
	#except:
	#	war = ''
	#data[year] = war

	t = 'pitching_standard.' + str(year)
	try:
		yd = soup.find(id=t)
		age = yd.find(attrs={'data-stat':'age'}).text
	except:
		age = ''
	data[year] = age
print(data)