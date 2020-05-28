class mouse:
    def __init__(self, ID):
         self.ID = ID   #Mouse ID (string)
         self.CID = ''  #Cage ID
         self.ET = True    #Eartag?
         self.sex = False   #False: Female, True: Male
         self.age = 0
         self.pregnant = False
         self.sacked = ''   #Blank, may be sacked (Potential), or already sacked (Sacked)
         self.DOS = ''     #Date of Sack
         self.genotyped = False
         self.runt = False
         self.comment = ''  #Comment entry

class cage:
    def __init__(self, CID):
        self.CID = CID   #Cage ID (string)
        self.mice = []  #vector of mouse ID strings in this cage
        self.total = 0    #Total number of mice in the cage
        self.breeding = False
        self.EC = ''    #Experimental Condition
        self.pups = 0   #Number of pups
        self.DOB = ''   #Pup date of birth
        self.WD = ''    #Wean date
