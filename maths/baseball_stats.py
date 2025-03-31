import numpy as np

class BasicHitting:
    #TODO: walk to strikout ratio
    @staticmethod
    #total bases
    def calc_pa(df):
        return df['AB'] + df['BB'] + df['HBP'] + df['SF'] + df['SH']
    
    @staticmethod
    #singles
    def calc_b1(df):
        return df['H'] - df['B2'] - df['B3'] - df['HR']
    
    @staticmethod
    #tatal bases
    def calc_tb(df):
        return BasicHitting.calc_b1(df) + (df['B2'] * 2) + (df['B3'] * 3) + (df['HR'] * 4)
    
    @staticmethod
    #runs produced
    def calc_rp(df):
        return df['R'] + df['RBI'] - df['HR']
    
    @staticmethod
    #stolen base attempts
    def calc_sba(df):
        return df['SB'] + df['CS']
    
    @staticmethod
    #extra base hits
    def calc_xbh(df):
        return df['B2'] + df['B3'] + df['HR']
    
    @staticmethod
    #extra base hit percentage
    def calc_xbh_pct(df):
        return np.where(df['H'] > 0 , np.round(BasicHitting.calc_xbh(df) / df['H'], 3), np.nan)

    @staticmethod
    #times on base
    def calc_tob(df):
        return df['H'] + df['BB'] + df['HBP']
    
    @staticmethod
    #home runs per hit
    def calc_hrh(df):
        return np.where(df['H'] > 0, np.round(df['HR'] / df['H'], 4), np.nan)
    
    @staticmethod
    #home runs per at bat
    def calc_hrab(df):
        return np.where(df['AB'] > 0, np.round(df['HR'] / df['AB'], 4), np.nan)

    @staticmethod
    #base runs
    def calc_br(df):
        A = df['H'] + df['BB'] + df['HBP'] + (df['IBB'] * 0.5) - df['HR']
        B = ((1.4 * df['TB']) - (0.6 * df['H']) - (3 * df['HR']) + (0.1 * (df['BB'] + df['HBP'] - df['IBB']))) + (0.9 * (df['SB'] - df['CS'] - df['GiDP'])) * 1.1
        C = df['AB'] - df['H'] + df['CS'] + df['GiDP']
        D = df['HR']
        return np.where(A + B > 0, np.round(((A * B) / (B + C)) + D, 3), np.nan)
    
    @staticmethod
    #batting average on balls in play
    def calc_babip(df):
        A = df['H'] - df['HR']
        B = df['AB'] - df['K'] - df['HR'] + df['SF']
        return np.where(B > 0, np.round(A / B, 3), np.nan)
    
    @staticmethod
    #equivalent average
    def calc_eqa(df):
        A = df['H'] + BasicHitting.calc_tb(df) + (1.5 * (df['BB'] + df['HBP'])) + df['SB'] + df['SH'] + df['SF']
        B = df['AB'] + df['BB'] + df['HBP'] + df['SH'] + df['SF'] + df['CS'] + (df['SB'] / 3)
        return np.where(B > 0, np.round(A / B, 3), np.nan)

    @staticmethod
    #batting average
    def calc_ba(df):
        return np.where(df['AB'] > 0, np.round(df['H'] / df['AB'], 3), np.nan)

    @staticmethod
    #on base percentage
    def calc_obp(df):
        return np.where(df['PA'] > 0, np.round((df['H'] + df['BB'] + df['HBP']) / df['PA'], 3), np.nan)

    @staticmethod
    #slugging percentage
    def calc_slg(df):
        return np.where(df['AB'] > 0, np.round(df['TB'] / df['AB'], 3), np.nan)

    @staticmethod
    #on base plus slugging
    def calc_ops(df):
        return BasicHitting.calc_obp(df) + BasicHitting.calc_slg(df)

    @staticmethod
    #isolated power
    def calc_iso(df):
        return BasicHitting.calc_slg(df) - BasicHitting.calc_ba(df)
    
    @staticmethod
    #plate apperance per strikeout
    def calc_paso(df):
        return np.where(df['K'] > 0, np.round(df['PA'] / df['K'], 3), np.nan)
    
    def calc_bbk(df):
        return np.where(df['K'] > 0, np.round(df['BB'] / df['K'], 3), np.nan) 

    @staticmethod
    #gross production average
    def calc_gpa(df):
        return np.where(BasicHitting.calc_slg(df) > 0, ((BasicHitting.calc_obp(df) * 1.8) + BasicHitting.calc_slg(df)) / 4, np.nan)

    @staticmethod
    #runs created
    def calc_rc(df):

        A = df['H'] + df['BB'] - df['CS'] + df['HBP'] - df['GiDP']
        B = (1.25 * BasicHitting.calc_b1(df)) + (1.69 * df['B2']) + (3.02 * df['B3']) + (3.73 * df['HR']) + (.29 * (df['BB'] - df['IBB'] + df['HBP'])) + (.492 * (df['SH'] + df['SF'] + df['SB'])) - (.04 * df['K'])
        C = df['AB'] + df['BB'] + df['HBP'] + df['SH'] + df['SF']

        TOP = ((2.4*C + A) * (3*C + B))
        
        return np.where(C > 0, (TOP/(9*C)) - .9*C, 0)

    @staticmethod
    #stolen base percentage
    def calc_sbp(df):
        return np.where(df['SBA'] > 0, df['SB'] / df['SBA'], np.nan)

    @staticmethod
    #total average
    def calc_ta(df):
        T = df['TB'] + df['HBP'] + df['BB'] + df['SB']
        B = df['AB'] - df['H'] + df['CS'] + df['GiDP']
        return np.where(B > 0, T / B, np.nan)

class BasicPitching:
    
    #innings pitched
    @staticmethod
    def calc_ip(df):
        return np.round(df['IPO'] / 3, 3)
    
    #decsions
    @staticmethod
    def calc_decisions(df):
        return df['W'] + df['L']
    
    #no decisions
    @staticmethod
    def calc_no_decisions(df):
        return df['G'] - BasicPitching.calc_decisions(df)
    
    #pitched at bats
    @staticmethod
    def calc_pab(df):
        return df['BF'] - df['BB'] - df['SF'] - df['SH'] - df['HBP']
    
    #component earned run average
    @staticmethod
    def calc_cera(df):
        PTB = .89 * (1.255 * (df['H'] - df['HR']) + 4 * df['HR']) + .56 * (df['BB'] + df['HBP'] - df['IBB'])
        A = (df['H'] + df['BB'] + df['HBP']) * PTB
        B = (df['BF'] * BasicPitching.calc_ip(df))
        return np.where(B > 0, np.round(9 * (A/B) - .56, 3), -.56)
    
    #defense independant earned run average
    @staticmethod
    def calc_dera(df):
        A = (13 * df['HR']) + (3 * (df['BB'] + df['HBP'])) - (2 * df['K'])
        return np.where(df['IPO'] > 0, np.round(3 + (A / BasicPitching.calc_ip(df)), 3), np.nan)

    #earned run average
    @staticmethod
    def calc_era(df):
        return np.where(df['IPO'] > 0, np.round(9 * (df['ER'] / BasicPitching.calc_ip(df)), 3), np.nan)
    
    #hits per nine innings
    @staticmethod
    def calc_h9(df):
        return np.where(df['IPO'] > 0, np.round(9 * (df['H'] / BasicPitching.calc_ip(df)), 3), np.nan)
    
    #home runs per nine innings
    @staticmethod
    def calc_hr9(df):
        return np.where(df['IPO'] > 0, np.round(9 * (df['HR'] / BasicPitching.calc_ip(df)), 3), np.nan)
    
    #strikeouts per nine innings
    @staticmethod
    def calc_k9(df):
        return np.where(df['IPO']> 0, np.round(9 * (df['K'] / BasicPitching.calc_ip(df)), 3), np.nan)
    
    #strikouts per game
    @staticmethod
    def calc_kg(df):
        return np.where(df['G'] > 0, np.round(df['K'] / df['G'], 3), np.nan)
    
    #home runs per game
    @staticmethod
    def calc_hrg(df):
        return np.where(df['G'] > 0, np.round(df['HR'] / df['G'], 3), np.nan)
    
    #runs allowed per game
    def calc_rag(df):
        return np.where(df['G'] > 0, np.round(df['R'] / df['G'], 3), np.nan)
    
    #opposing batting average
    def calc_oba(df):
        return np.where(BasicPitching.calc_pab(df) > 0, np.round( df['H'] / BasicPitching.calc_pab(df), 3), np.nan)
    
    #opposing batting average on balls in play
    def calc_pbabip(df):
        A = df['H'] - df['HR']
        B = BasicPitching.calc_pab(df) - df['K'] - df['SF']
        return np.where(B > 0, np.round(A / B, 3), np.nan)
    
    #power finesse ration
    def calc_pfr(df):
        A = df['K'] + df['BB']
        return np.where(df['IPO'] > 0, np.round(A / BasicPitching.calc_ip(df), 3), np.nan)

    #runs per 9 innings
    def calc_r9(df):
        return np.where(df['IPO'] > 0, np.round(9 * (df['R'] / BasicPitching.calc_ip(df)), 3), np.nan)
    
    #walks per 9 innings
    def calc_bb9(df):
        return np.where(df['IPO'] > 0, np.round(9 * (df['BB'] / BasicPitching.calc_ip(df)), 3), np.nan)
    
    #batters faced per 9 innings
    def calc_bf9(df):
        return np.where(df['IPO'] > 0, np.round(9 * (df['BF'] / BasicPitching.calc_ip(df)), 3), np.nan)
    
    #walks and hits per innings pitched
    def calc_whip(df):
        return np.where(df['IPO'] > 0, np.round((df['BB'] + df['H']) / BasicPitching.calc_ip(df), 3), np.nan)
    
    #win percentage
    def calc_wp(df):
        return np.where(BasicPitching.calc_decisions(df) > 0, np.round(df['W']/BasicPitching.calc_decisions(df), 3), np.nan)
    
    #walk to strikout ratio
    def calc_bbk(df):
        return np.where(df['K'] > 0, np.round(df['BB']/df['K'], 3), np.nan)
    
    #opposing on base percentage
    def calc_obpa(df):
        return np.where(BasicPitching.calc_pab(df) > 0, np.round((df['H'] + df['BB'] + df['HBP']) / BasicPitching.calc_pab(df), 3), np.nan)
