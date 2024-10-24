class basic_hitting:
    def __init__(self, stats):
        #store provided stats 
        self.g = stats['g']
        self.ab = stats['ab']
        self.r = stats['r']
        self.h = stats['h']
        self.b2 = stats['b2']
        self.b3 = stats['b3']
        self.hr = stats['hr']
        self.rbi = stats['rbi']
        self.sb = stats['sb']
        self.cs = stats['cs']
        self.bb = stats['bb']
        self.k = stats['k']
        self.ibb = stats['ibb']
        self.hbp = stats['hbp']
        self.sh = stats['sh']
        self.sf = stats['sf']
        self.gidp = stats['gidp']
        #calculate the easy ones that don't require division
        self.pa = stats['ab'] + stats['bb'] + stats['hbp'] + stats['sf'] + stats['sh']
        self.rp = stats['r'] + stats['rbi'] - stats['hr']
        self.b1 = stats['h'] - stats['b2'] - stats['b3'] - stats['hr']
        self.sba = stats['sb'] + stats['cs']
        self.tob = stats['h'] + stats['bb'] + stats['hbp']
        self.tb = self.b1 + (stats['b2'] * 2) + (stats['b3'] * 3) + (stats['hr'] * 4)
    
    #base runs
    def calc_br(self):
        if self.ab > 0:
            a = self.h = self.bb + self.hbp + (self.ibb * .5) - self.hr
            b = ((1.4 * self.tb) - (.6 * self.h) - ( 3 * self.hr) + (.1 * (self.bb + self.hbp - self.ibb)) + (.9 * (self.sb - self.cs - self.gidp))) * 1.1
            c = self.ab - self.h + self.cs + self.gidp
            d = self.hr
            return round(((a * b) / (b + c)) + d, 3) if a+b > 0 else None
        else:
            return None

    #batting average  
    def calc_ba(self):
        return round(self.h / self.ab, 3) if self.ab > 0 else None
    
    #batting average on balls in play
    def calc_babip(self):
        if self.ab > 0:
            t = self.h - self.hr
            b = self.ab - self.k - self.hr + self.sf
            return round(t/b, 3) if b>0 else 0
        else:
            return None
    
    #walks per strikeout
    def calc_bbk(self):
        return self.bb / self.k if self.k > 0 else self.bb
    
    #equivalent average
    def calc_eqa(self):
        t = self.h + self.tb + (1.5 * (self.bb + self.hbp)) + self.sb + self.sh + self.sf
        b = self.ab + self.bb + self.hbp + self.sh + self.sf + self.cs + (self.sb / 3)
        return t/b if b>0 else None

    #on base percentage
    def calc_obp(self):
        return round((self.h + self.bb + self.hbp) / self.pa, 3) if self.pa > 0 else None
   
    #slugging percentage
    def calc_slg(self):
        return round(self.tb / self.ab, 3) if self.ab > 0 else None
    
    #gross production average
    def calc_gpa(self):
        return ((self.calc_obp() * 1.8) + self.calc_slg()) / 4 if self.calc_slg() > 0 else None

    #at bats per homerun
    def calc_abhr(self):
        return round(self.ab / self.hr, 2) if self.hr > 0 else self.ab
    
    #hits per homerun
    def calc_hhr(self):
        return round(self.h / self.hr, 2) if self.hr > 0 else self.h
    
    #isolated something
    def clac_iso(self):
        return self.calc_slg() - self.calc_ba()

    #on base plus slugging
    def calc_ops(self):
        obp = self.calc_obp()
        slg = self.calc_slg()
        if obp is not None and slg is not None:
            return obp + slg
        else:
            return None

    #plate appearances per walks
    def calc_paso(self):
        return self.pa / self.k if self.k > 0 else self.pa

    #runs created
    def calc_rc(self):
        a = self.h + self.bb - self.cs + self.hbp - self.gidp
        b = (1.25 * self.b1) + (1.69 * self.b2) + (3.02 * self.b3) + (3.73 * self.hr) + (.29 * (self.bb - self.ibb + self.hbp)) + (.492 * (self.sh + self.sf + self.sb)) - (.04 * self.k)
        c = self.pa * 9

        top = ((2.4 * c) + a) * ((3 * c) + b)
        btm = 9*c

        return (top/btm) * (.9 * c) if btm>0 else 0

    #stolen base percentage
    def calc_sbp(self):
        return self.sb / self.sba if self.sba > 0 else None
    
    #total average
    def calc_ta(self):
        t = self.tb + self.hbp + self.bb + self.sb
        b = self.ab - self.h + self.cs + self.gidp
        return t/b if b>0 else None


    