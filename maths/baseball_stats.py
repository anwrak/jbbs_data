import numpy as np

class BasicHitting:
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
