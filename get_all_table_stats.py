from bs4 import BeautifulSoup
import requests
import re
import pickle

# This file gets all desired stats for David Aardsma.
## Output is a dict with k, v = year, python list of stats.
### Uncomment print or pickle functions below.
#### Next steps: wrap this in a function and scale to many payers.

url_aards = 'https://www.baseball-reference.com/players/a/aardsda01.shtml'
r = requests.get(url_aards).text
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

# Optional print statement.
#for key, value in data.items():
#	print("Dict Key: " + str(key), "     Dict Value: " + str(value))

# Optional pickle statment.
#filename = 'david_aardsma.pkl'
#with open(filename, 'wb') as f_obj:
#	pickle.dump(data, f_obj)