from bs4 import BeautifulSoup
import requests
import re

# This file gets all of DA's salary data available.
url_aards = 'https://www.baseball-reference.com/players/a/aardsda01.shtml'
r = requests.get(url_aards).text
comm = re.compile("<!--|-->")
cleaned = comm.sub("", r)
soup = BeautifulSoup(cleaned, 'lxml')

years = range(2000, 2018)
data = {}
for year in years:
	t = "pitching_value." + str(year)
	try:
		yd = soup.find(id=t)
		sal = yd.find(attrs={'data-stat':'Salary'})
	except:
		sal = ''
	else:
		sal = sal.text.strip('$')
		sal = ''.join(sal.split(','))
	data[year] = sal