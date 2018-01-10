from bs4 import BeautifulSoup
import requests
import re

# This file gets the first year of salary data (2004) from David Aardsma's page.
url_aards = 'https://www.baseball-reference.com/players/a/aardsda01.shtml'
r = requests.get(url_aards).text
comm = re.compile("<!--|-->")
cleaned = comm.sub("", r)
soup = BeautifulSoup(cleaned, 'lxml')
b = soup.find(id='pitching_value.2004')
q = b.find(attrs={'data-stat':'Salary'}).text