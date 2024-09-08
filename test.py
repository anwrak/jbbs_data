import pandas as pd

#import people data from csv
import_people = pd.read_csv('datafiles/People.csv', encoding='latin-1')
import_generations = pd.read_csv('datafiles/custom/generation.csv', encoding='latin-1')

#remove non-players, remove unneeded columns
people_df = import_people[~import_people['playerID'].str.endswith('99')].drop(['ID', 'deathYear', 'deathMonth', 'deathDay', 'deathCountry', 'deathState', 'deathCity', 'nameGiven'], axis=1)
print(people_df)