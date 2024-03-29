class mouse:
    def __init__(self, ID):
        self.ID = ID  # Mouse ID (string)
        self.ET = True  # Eartag (bool)
        self.sex = False  # False: Female, True: Male
        self.age = 0  # str or int (status or age)
        self.pregnant = False
        self.sacked = ''  # Sack status
        self.genotyped = False
        self.runt = False
        self.DOD = ''   #Date of Death


class cage:
    def __init__(self, CID):
        self.CID = CID  # Cage ID (string)
        self.pri = 1000000    #Cage Priority/print order (int)
        self.mice = []  # vector of mouse IDs
        self.color = 'white'  # X11 color name
        self.pups = 0  # Number of pups
        self.DOB = ''  # Pup date of birth
        self.WD = '' #Pup wean date (DOB+25)
