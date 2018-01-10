import pandas as pd
import pickle
import numpy as np

# Hack display to see all columns without text wrapping.
pd.set_option('display.width', 1000)

# Open pickled file of DA's scraped data.
filename = 'david_aardsma.pkl'
with open(filename, 'rb') as f_obj:
	data = pickle.load(f_obj)

columns = ['year', 'age', 'team', 'wins', 'losses', 'gp',
			'wlp', 'era', 'ip', 'so', 'so9', 'war',
			'salary', 'awards']

# Load into DataFrame.
df = pd.DataFrame.from_dict(data, orient='index')
df = df.reset_index()
df.columns = columns

# next_yr_sal is next available salary data.
## Convert to an int.
df['next_yr_sal'] = (df.salary.transform(lambda s: s.shift(-1)))
df['next_yr_sal'] = df['next_yr_sal'].str.strip('$').str.split(',').str.join('')

# Drop old salary column.
df.drop('salary', inplace=True, axis=1)

# league_min is the league minimum given the year.
## Merge a new df onto the right of the df.
lm_dict = {	2000: 200000,
			2001: 300000,
			2002: 300000,
			2003: 300000,
			2004: 316000,
			2005: 327000,
			2006: 380000,
			2007: 390000,
			2008: 400000,
			2009: 400000,
			2010: 414000,
			2011: 480000,
			2012: 480000,
			2013: 480000,
			2014: 507500,
			2015: 507500,
			2016: 535000,
			}
lm = pd.DataFrame.from_dict(data=lm_dict, orient='index')
lm = lm.reset_index()
lm = lm.rename(columns={'index': "year", 0: 'ny_league_min'})
df = df.merge(lm, how='outer', on='year')


# Drop rows with no useful stats or salary data.
df = df.replace('', np.nan)
df = df.dropna(subset=['next_yr_sal', 'age', 'team'], axis=0)


# sal_delta is the difference above year's league_min.
df['sal_delta'] = df['next_yr_sal'].astype(int) - df['ny_league_min'].astype(int)


# Reset index.
df = df.reset_index(drop=True)


#### DataFrame for one player is now ready to use.
print(df)