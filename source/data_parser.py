import pandas as pd
from objects import *

#Input: pandas data frames df (mouse data) and df2 (cage data)
#Output: dict of mouse objects, dict of cage objects, and dict of conditions
def gen_objs(df, df2):
    mice = {}      #empty dict of mouse objects
    cages = {}     #empty dict of cage objects
    conds = {}      #condition/status dict (key: status, value: (Color, Priority integer))

    #Construct and assign mouse vectors to cages
    c_ls = df['Cage ID'].tolist()      #list of all cages including repeats
    m_ls = df['Mouse ID'].tolist()      #list of all mouse IDs
    
    #Loop to initalize conditions dict
    pri = 0
    for i in range(len(df2['Condition'].tolist())):
        if not isinstance(df2['Condition'][i], float):
            key = str(df2['Condition'][i]).lower()
            if key not in conds.keys():
                conds[key] = (str(df2['Color'][i]).lower(), int(pri))
                pri+=1

    #Loop to generate cage dict from mouse df
    for i in range(len(c_ls)):
        CID = str(c_ls[i])
        if CID not in cages.keys():    #Construct new entry if no key
            cages[CID] = cage(CID)
        cages[CID].mice.append(i)

    #Add cages exclusive to the cage df (not in mouse df), so these cages have no mice
    cdf_ls = df2['Cage ID'].tolist()
    for CID in cdf_ls:
        CID = str(CID)
        if CID not in cages.keys():
            cages[CID] = cage(CID)

    #Update remaining cage attributes from cage df
    for i in range(len(cdf_ls)):
        key = str(df2['Cage ID'][i])
        if not isinstance(df2['Status/Condition'][i], float):
            status = str(df2['Status/Condition'][i]).lower()     #CONVERT TO COLOR LATER
            cages[key].status = status
            if status in conds.keys():
                cages[key].pri = conds[status][1]
        cages[key].pups = df2['Number of Pups'][i]
        cages[key].DOB = df2['Pup DOB'][i]
        cages[key].WD = df2['Wean Date'][i]

    #Loop to initalize all mice objects
    for i in range(len(m_ls)):
        new_mouse = mouse(str(m_ls[i]))
        new_mouse.CID = str(c_ls[i])
        if str(df['Ear Tag?'][i]).lower() in ('n', 'no'):
            new_mouse.ET = False
        if str(df['Sex'][i]).lower() == 'm':     #False: Female, True: Male
            new_mouse.sex = True
        if not isinstance(df['Age (days)'][i], float):
            if isinstance(df['Age (days)'][i], str):
                new_mouse.age = str(df['Age (days)'][i])
            else:
                new_mouse.age = int(df['Age (days)'][i])
        if str(df['Pregnant?'][i]).lower() in ('y', 'yes'):
            new_mouse.pregnant = True
        new_mouse.sacked = str(df['Sacked Status: Potential (P), Sacked (S), Sacrificed (D)'][i]).lower() #Blank, potential for sack (p), or already sacked (s)
        if str(df['Genotyped?'][i]).lower() in ('y', 'yes'):
            new_mouse.genotyped = True
        if str(df['Runt?'][i]).lower() in ('y', 'yes'):
            new_mouse.runt = True
        if isinstance(df['Date of Death'], str) and not str(df['Date of Death'][i]).isspace():
            new_mouse.DOD = str(df['Date of Death'][i])
        mice[i] = new_mouse
            
    return mice, cages, conds


def parse_data(filename):
    file = open('../' + filename, 'rb')

    mice_data = pd.read_excel(file, sheet_name = 0, skiprows = 1)  #data frame generation (skip first row)
    mice_data.dropna(axis=0, how = 'all', inplace = True)   #drop blank rows and reset indices
    mice_data.reset_index(drop = True, inplace = True)

    cage_data = pd.read_excel(file, sheet_name = 1, skiprows = 1)
    cage_data.dropna(axis=0, how = 'all', inplace=True)
    cage_data.reset_index(drop = True, inplace = True)

    #Construct and sort mice/cage objects
    mice, cages, conds = gen_objs(mice_data, cage_data)

    return mice, cages, conds
