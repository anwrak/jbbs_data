class basic_hitting:
    def __init__(self, g, ab, r, h, b2, b3, hr, rbi, sb, cs, bb, k, ibb, hbp, sh, sf, gidp):
        #store provided stats 
        self.g = g
        self.ab = ab
        self.r = r
        self.h = h
        self.b2 = b2
        self.b3 = b3
        self.hr = hr
        self.rbi = rbi
        self.sb = sb
        self.cs = cs
        self.bb = bb
        self.k = k
        self.ibb = ibb
        self.hbp = hbp
        self.sh = sh
        self.sf = sf
        self.gidp = gidp
        self.pa = ab + bb + hbp + sf + sh
        self.rp = r + rbi - hr
        self.b1 = h - b2 - b3 - hr
        self.sba = sb + cs
        self.tob = h + bb + hbp
        self.tb = self.b1 + (b2 * 2) + (b3 * 3) + (hr * 4)
    
    def calc_br(self):
        if self.ab > 0:
            a = self.h = self.bb + self.hbp + (self.ibb * .5) - self.hr
            b = ((1.4 * self.tb) - (.6 * self.h) - ( 3 * self.hr) + (.1 * (self.bb + self.hbp - self.ibb)) + (.9 * (self.sb - self.cs - self.gidp))) * 1.1
            c = self.ab - self.h + self.cs + self.gidp
            d = self.hr
            return round(((a * b) / (b + c)) + d, 3) if a+b > 0 else None
        else:
            return None
        
    def calc_ba(self):
        return round(self.h / self.ab, 3) if self.ab > 0 else None
    
    def calc_babip(self):
        if self.ab > 0:
            t = self.h - self.hr
            b = self.ab - self.k - self.hr + self.sf
            return round(t/b, 3) if b>0 else 0
        else:
            return None
    
    #TODO: bbk calc

    def calc_bbk(self):
        return 0
    
    #TODO:eqa calc

    def calc_obp(self):
        return round((self.h + self.bb + self.hbp) / self.pa, 3) if self.pa > 0 else None
   
    def calc_slg(self):
        return round(self.tb / self.ab, 3) if self.ab > 0 else None
    
    #TODO:gpa calc

    def calc_abhr(self):
        return round(self.ab / self.hr, 2) if self.hr > 0 else None
    
    def calc_hhr(self):
        return round(self.h / self.hr, 2) if self.hr > 0 else None
    
    #TODO:iso calc

    def calc_ops(self):
        obp = self.calc_obp()
        slg = self.calc_slg()
        if obp is not None and slg is not None:
            return obp + slg
        else:
            return None

    #TODO:paso calc

    #TODO:rc calc

    #TODO:sbp calc
    
    #TODO:ta calc



    