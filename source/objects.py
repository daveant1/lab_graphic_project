class mouse:
    def __init__(self, ID):
        self.ID = ID  # Mouse ID (string)
        self.idx = 0
        self.CID = ''  # Cage ID (string)
        self.ET = True  # Eartag (bool)
        self.sex = False  # False: Female, True: Male
        self.age = ''  # str or int (status or age)
        self.pregnant = False
        self.sacked = ''  # Sack status
        self.genotyped = False
        self.runt = False


class cage:
    def __init__(self, CID):
        self.CID = CID  # Cage ID (string)
        self.mice = []  # vector of mouse IDs
        self.status = ''  # status or X11 color name
        self.pups = 0  # Number of pups
        self.DOB = ''  # Pup date of birth