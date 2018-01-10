import pandas as pd
import pickle

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

print(df)


######NOTES######
# Next steps: massage DF to predict next year's sal from prev yr's stats
# Add League mimimum...maybe calculate salary delta from minimum?