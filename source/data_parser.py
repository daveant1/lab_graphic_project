import pandas as pd
from objects import *

#Input: pandas data frames df_m (mouse data) and df_c (cage data)
#Output: dict of mouse objects, dict of cage objects, and dict of conditions
def gen_objs(df_m, df_c):
    mice = {}      #empty dict of mouse objects
    cages = {}     #empty dict of cage objects
    conds = {}      #condition/status dict (key: status, value: (Color, Priority integer))

    #Initalize conditions dict
    pri = 1
    cond_ls = df_c['Condition'].tolist()
    for i in range(len(cond_ls)):
        cond = cond_ls[i]
        if not pd.isnull(cond) and not str(cond).isspace():
            conds[pri] = str(df_c['Color'][i]).lower()
            pri+=1

    #Generate cage dict from mouse df
    c_ls = df_m['Cage ID'].tolist()      #list of all cages including repeats
    for i in range(len(c_ls)):
        CID = str(c_ls[i])
        if CID not in cages.keys():    #Construct new entry if no key
            cages[CID] = cage(CID)
        cages[CID].mice.append(i)

    #Add cages exclusive to the cage df (not in mouse df), so these cages have no mice
    cdf_ls = df_c['Cage ID'].tolist()
    for CID in cdf_ls:
        CID = str(CID)
        if CID not in cages.keys():
            cages[CID] = cage(CID)

    #Update remaining cage attributes from cage df
    for i in range(len(cdf_ls)):
        key = str(df_c['Cage ID'][i])
        if not pd.isnull(df_c['Status/Condition'][i]):
            status = str(df_c['Status/Condition'][i]).lower()
            cages[key].status = status
            if status in conds.keys():
                cages[key].pri = conds[status][1]
        cages[key].pups = df_c['Number of Pups'][i]
        cages[key].DOB = df_c['Pup DOB'][i]
        cages[key].WD = df_c['Wean Date'][i]
    
    #Initalize all mouse objects
    m_ls = df_m['Mouse ID'].tolist()      #list of all mouse IDs
    for i in range(len(m_ls)):
        new_mouse = mouse(str(m_ls[i]))
        new_mouse.CID = str(c_ls[i])
        if str(df_m['Ear Tag?'][i]).lower() in ('n', 'no'):
            new_mouse.ET = False
        if str(df_m['Sex'][i]).lower() == 'm':     #False: Female, True: Male
            new_mouse.sex = True
        if not pd.isnull(df_m['Age (days)'][i]):          #Check if cell is blank
            if isinstance(df_m['Age (days)'][i], str):    #Check if cell is string or whitespace (whitespace accounted for before printing)
                new_mouse.age = str(df_m['Age (days)'][i])
            else:
                new_mouse.age = int(df_m['Age (days)'][i])
        if str(df_m['Pregnant?'][i]).lower() in ('y', 'yes'):
            new_mouse.pregnant = True
        new_mouse.sacked = str(df_m['Sacked Status: Potential (P), Sacked (S), Died (D)'][i]).lower() #Blank, potential for sack (p), already sacked (s), or sacrificed (d)
        if str(df_m['Genotyped?'][i]).lower() in ('y', 'yes'):
            new_mouse.genotyped = True
        if str(df_m['Runt?'][i]).lower() in ('y', 'yes'):
            new_mouse.runt = True
        new_mouse.DOD = str(df_m['Date of Death'][i])
        
        mice[i] = new_mouse

    return mice, cages, conds


def parse_data(filename):
    file = open(filename, 'rb')

    #No longer necessary to remove empty rows; Switch to openpyxl engine for reading? Move all this logic over to error detection functions?
    mice_data, cage_data = pd.read_excel(file, sheet_name = 'Mice', skiprows = 1, engine = 'xlrd'), pd.read_excel(file, sheet_name = 'Cages', skiprows = 1, engine = 'xlrd')

    #Construct and sort mice/cage objects
    return gen_objs(mice_data, cage_data)
