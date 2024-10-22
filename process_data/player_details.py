
import pandas as pd

#import people data from csv
#TODO: Rename Enrique hernandez to Kike hernandez
k = ['playerID', 'birthYear', 'birthMonth', 'birthDay', 'weight', 'height', 'birthCountry', 'birthCity', 'birthState', 'nameFirst', 'nameLast', 'bats', 'throws', 'debut', 'finalGame', 'retroID', 'bbrefID']
import_people = pd.read_csv('./datafiles/People.csv', encoding='latin-1', usecols=k)

#import juniors data and convert to a list
import_juniors =  pd.read_csv('./custom data/juniors.csv')
juniors = import_juniors['playerid'].values.tolist()

#import birth region file
import_regions = pd.read_csv('./custom data/regions.csv')

#import salary data and sum by user id
import_salary = pd.read_csv('./datafiles/Salaries.csv', encoding='latin-1', usecols=['playerID', 'salary'])
salary = import_salary.groupby(['playerID'], as_index=False).sum()

#import hall of fame and figure out who be HOF
import_hof = pd.read_csv('./datafiles/HallOfFame.csv', encoding='latin-1')
hof = import_hof[(import_hof['inducted'] == 'Y')]
#remove preliminary vote records
hof = hof[~hof['needed_note'].fillna('none').str.contains('Preliminary')][['playerID', 'inducted']]

#import team information
import_team = pd.read_csv('./datafiles/Teams.csv', encoding='latin-1')
teams = import_team.loc[import_team.groupby(['teamID'])['yearID'].idxmax()][['teamID', 'yearID', 'name']]

#import appearances
import_appearances = pd.read_csv('./datafiles/Appearances.csv', encoding='latin-1')
appearances = import_appearances[['playerID', 'teamID', 'G_all']].copy().groupby(['playerID', 'teamID'], as_index=False).sum()
appearances = appearances.loc[appearances.groupby('playerID')['G_all'].idxmax()].drop(['G_all'], axis=1).merge(teams, how='left', on='teamID').drop(['yearID'], axis=1)

#see if player appeared in latest year
max_year = import_appearances['yearID'].max()
current_players = import_appearances[['playerID', 'yearID']].groupby(['playerID'], as_index=False).max()
current_players['is_current'] = current_players.apply(lambda x: 1 if x['yearID'] == max_year else 0, axis=1)
current_players.drop(['yearID'], inplace=True, axis=1)

#position appearances
position = import_appearances.drop(['yearID', 'teamID', 'lgID', 'G_all', 'G_batting', 'G_defense', 'G_of'], axis=1).groupby(['playerID'], as_index=False).sum()
position['pos_id'] = position.drop(['playerID', 'GS'], axis=1).idxmax(axis=1)

#import batting data
batting_import = pd.read_csv('./datafiles/Batting.csv', encoding='latin-1', usecols=['playerID', 'yearID', 'AB', 'BB', 'HBP', 'SF', 'SH'])
batting = batting_import.drop(['yearID'], axis=1).groupby('playerID', as_index=True).sum().sum(axis=1).reset_index()
batting = batting.rename(columns={0:'PA'})

#calculate avg pa per season
b_sig = batting_import.groupby(['playerID', 'yearID'], as_index=True).sum().sum(axis=1).reset_index()
b_sig = b_sig.drop(['yearID'], axis=1).groupby(['playerID'], as_index=False).mean()
b_sig = b_sig.rename({0:'avg_pa'}, axis=1)

#import pitching data
pitching_import = pd.read_csv('./datafiles/Pitching.csv', encoding='latin-1', usecols=['playerID', 'yearID', 'IPouts'])
pitching = pitching_import.drop(['yearID'], axis=1).groupby(['playerID'], as_index=False).agg(PIPO = ('IPouts', 'sum'))

#calculate avg ip per season
p_sig = pitching_import[['playerID', 'yearID', 'IPouts']].groupby(['playerID', 'yearID'], as_index=False).sum()
p_sig['avg_inn'] = p_sig.apply(lambda x: x['IPouts']/3, axis=1)
p_sig = p_sig.drop(['yearID', 'IPouts'], axis=1).groupby(['playerID'], as_index=False).mean()

#import fielding data
fielding_import = pd.read_csv('./datafiles/Fielding.csv', encoding='latin-1', usecols=['playerID', 'InnOuts'])
fielding = fielding_import.groupby(['playerID'], as_index=False).agg(FIPO = ('InnOuts', 'sum'))

#player functions
def jr(i, n): #this function takes in the user id and last name. if a junior it appends jr.
    if i in juniors:
        return f"{n} Jr."
    else:
        return n
    
def gen(x): #determines the players generation based upon birth year

    if 1700 <= x <= 1882:
        return 'Pre-Generational'
    elif 1883 <= x <= 1900:
        return 'Lost Generation'
    elif 1901 <= x <= 1927:
        return 'Greatest Generation'
    elif 1928 <= x <= 1945:
        return 'Silent Generation'
    elif 1946 <= x <= 1964:
        return 'Baby Boomers'
    elif 1965 <= x <= 1980:
        return 'Gen X'
    elif 1981 <= x <= 1996:
        return 'Millenial'
    elif 1997 <= x <= 2012:
        return 'Gen Z'
    elif 2013 <= x <= 2025:
        return 'Gen Alpha'
    else:
        return 'Unknown'
    
def pos(p, gs, gp): #determines player position
    
    if (p == 'G_p'):
        if gp == 0:
            pid = 'PH'
        elif gs/gp < .25:
            pid = 'RP'
        else:
            pid = 'SP'
    else: 
        pid = p.replace('G_', '').upper()
    return pid

def pos_group(x): #groups positions
    if x in ('SP', 'RP', 'C'):
        return 'Battery'
    elif x in ('1B', '2B', '3B', 'SS'):
        return 'Infield'
    elif x in ('CF', 'LF', 'RF'):
        return 'Outfield'
    elif x in ('DH', 'PH', 'PR'):
        return 'Offensive'
    else:
        return 'Unknown'
    
def sig_batter(x, t):
    if t not in ['SP', 'RP']:
        return 1 if x > 200 else 0
    else:
        return 0

def sig_pitcher(x, t):
    if t == 'RP':
        return 1 if x > 40 else 0
    elif t == 'SP':
        return 1 if x > 125 else 0
    else: 
        return 0
    
#remove non-players, remove unneeded columns
people_df = import_people[~import_people['playerID'].str.endswith('99')].copy()

#fix blanks and cast as integer where appropriate
people_df['birthYear'] = people_df['birthYear'].fillna(0).astype(int)
people_df['birthMonth'] = people_df['birthMonth'].fillna(0).astype(int)
people_df['birthDay'] = people_df['birthDay'].fillna(0).astype(int)
people_df['weight'] = people_df['weight'].fillna(0).astype(int)
people_df['height'] = people_df['height'].fillna(0).astype(int)
people_df['birthCountry'] = people_df['birthCountry'].fillna('Unknown').apply(lambda x: x if x != 'Ukriane' else 'Ukraine')
people_df['birthCity'] = people_df['birthCity'].fillna('Unknown')
people_df['birthState'] = people_df['birthState'].fillna('NA')
people_df['birthCity'] = people_df.apply(lambda x: f"{x['birthCity']}, {x['birthState']}", axis=1)
people_df['nameFirst'] = people_df['nameFirst'].fillna('Unknown')
people_df['bats'] = people_df['bats'].fillna('U')
people_df['throws'] = people_df['throws'].fillna('U')
people_df['bbrefID'] = people_df['bbrefID'].fillna('xxx1234')
people_df['debutDate'] = people_df['debut'].fillna('1800-01-01')
people_df['finalGame'] = people_df['finalGame'].fillna('1800-01-01')

#concatenate birth day
people_df['birthDate'] = people_df.apply(lambda x: f"{x['birthYear']}-{str(x['birthMonth']).zfill(2)}-{str(x['birthDay']).zfill(2)}", axis=1)

#juniorize and make the full name
people_df['nameLast'] = people_df.apply(lambda x: jr(x['playerID'], x['nameLast']), axis=1)
people_df['fullName'] = people_df.apply(lambda x: f"{x['nameFirst']} {x['nameLast']}", axis=1)

#determine player generation
people_df['generation'] = people_df['birthYear'].apply(lambda x: gen(x))

#determine birth region
people_df = people_df.merge(import_regions, how='left', left_on='birthCountry', right_on='country')

#append salary data
people_df = people_df.merge(salary, how='left', on='playerID').fillna(0)

#append salary data
people_df = people_df.merge(current_players, how='left', on='playerID').fillna(0)

#append hall of fame
people_df = people_df.merge(hof, how='left', on='playerID').fillna('N')

#append primary player team
people_df = people_df.merge(appearances, how='left', on='playerID')

#append plate appearances
people_df = people_df.merge(batting, how='left', on='playerID').fillna(0)

#append innings pitched
people_df = people_df.merge(pitching, how='left', on='playerID').fillna(0)

#append fielding innings
people_df = people_df.merge(fielding, how='left', on='playerID').fillna(0)

#figure out primary position
position['position'] = position.apply(lambda x: pos(x['pos_id'], x['GS'], x['G_p']), axis=1).fillna('UK')
position['pitcher'] = position.apply(lambda x: 'Y' if (x['position']=='RP')|(x['position']=='SP') else 'N', axis=1)
position['position_group'] = position.apply(lambda x: pos_group(x['position']), axis=1)
people_df = people_df.merge(position[['playerID', 'position', 'pitcher', 'position_group']], how='left', on='playerID')

#append avg pa and flag significant
people_df = people_df.merge(b_sig, how='left', on='playerID')
people_df['sig_batter'] = people_df.apply(lambda x: sig_batter(x['avg_pa'], x['position']), axis=1)

#append avg innings pitched and flag significant
people_df = people_df.merge(p_sig, how='left', on='playerID')
people_df['sig_pitcher'] = people_df.apply(lambda x: sig_pitcher(x['avg_inn'], x['position']), axis=1)

#rename columns as needed
people_df = people_df.rename(columns={'inducted':'hof', 'name':'teamName', 'region':'birthRegion'})

#order the columns
people_df = people_df[['playerID', 'nameFirst', 'nameLast', 'fullName', 'birthDate', 'birthCity', 'birthState', 'birthCountry','birthRegion', 'generation', 'is_current', 'sig_batter', 'sig_pitcher', 'weight', 'height', 'bats', 'throws', 'debutDate', 'finalGame', 'hof', 'pitcher', 'position', 'position_group', 'PA', 'FIPO', 'PIPO', 'salary', 'teamID', 'teamName', 'bbrefID', 'retroID']]

#output to csv
people_df.to_csv('./output/player_details.csv', index=False)