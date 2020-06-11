import pandas as pd
from objects import *

#Input: pandas data frame from colony_data
#Output: Vector of mouse objects and vector of cage objects
def gen_objs(df):
    mice = {}      #empty dict of mouse objects
    cages = []     #empty vector of cage objects
    col_list = df.columns.tolist()

#Construct and assign mouse vectors to cages
    c_ls = df['Cage ID'].tolist()      #list of all cages including repeats
    m_ls = df['Mouse ID'].tolist()      #list of all mouse IDs

    #Loop to generate new cage entry based on new Cage ID
    prev_cage = str(c_ls[0])
    new_cage = cage(str(c_ls[0]))
    self_mice = []
    for i in range(len(c_ls)):
        CID = str(c_ls[i])    #Cage ID
        if CID != prev_cage:
            new_cage.mice = self_mice
            new_cage.total = len(self_mice)
            cages.append(new_cage)
            new_cage = cage(CID)
            self_mice = []      #vector of mice specific to one cage
            prev_cage = CID

        self_mice.append(str(m_ls[i]))

    #set members and append for final cage
    new_cage.mice = self_mice
    new_cage.total = len(self_mice)
    cages.append(new_cage)

    #Loop to initalize all mice objects
    for i in range(len(m_ls)):
        new_mouse = mouse(str(m_ls[i]))
        new_mouse.CID = str(c_ls[i])
        if df['Ear Tag?'][i] == 'NO':
            new_mouse.ET = False
        if df['Sex'][i] == 'M':     #False: Female, True: Male
            new_mouse.sex = True
        new_mouse.age = int(df['Age (days)'][i])
        if df['Pregnant?'][i] == 'YES':
            new_mouse.pregnant = True
        new_mouse.sacked = df['Sacked Status (Blank, Potential, Sacked)'][i]   #Blank, may be sacked (Potential), or already sacked (Sacked)
        new_mouse.DOS = df['Date of Sack'][i]
        if df['Genotyped?'][i] == 'YES':
            new_mouse.genotyped = True
        if df['Runt?'][i] == 'YES':
            new_mouse.runt = True
        new_mouse.comment = df['Comments'][i] #Comment entry
        mice[str(m_ls[i])] = new_mouse
    return mice, cages

#This function fills in the remaining info for the cage objects from the second excel sheet
#Input: pandas data frame of cages sheet, unfinished vector of cages
#Output: finished vector of cages
def finish_cages(df, cages):
    for i in range(len(cages)):
        cages[i].status = df['Status/Condition'][i]
        # print(type(cages[i].status))
        cages[i].pups = df['Number of Pups'][i]
        cages[i].DOB = df['Pup DOB'][i]
        cages[i].WD = df['Wean Date (DOB + 28 d)'][i]
    return cages

def parse_data(filename):
    file = open(filename, 'rb')
    mice_data = pd.read_excel(file, sheet_name = 'Mice', skiprows = 1)  #data frame generation (skip first row)
    #usecols = ['Mouse ID', 'Cage ID', 'Ear Tag?', etc.]
    cage_data = pd.read_excel(file, sheet_name = 'Cages', skiprows = 1)


    mice, cages = gen_objs(mice_data)
    final_cages = finish_cages(cage_data, cages)
    # for c in final_cages:
    #     print(vars(c))
    # for m in mice.keys():
    #     print(vars(mice[m]))
    return mice, final_cages
