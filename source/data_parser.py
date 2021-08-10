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
            if cond not in conds.keys():
                conds[cond] = (str(df_c['Color'][i]).lower(), pri)
            pri+=1

    #Generate cage dict from mouse df
    c_ls = df_m['Cage ID'].tolist()
    cdf_ls = df_c['Cage ID'].tolist()
    cid_set = set(c_ls + cdf_ls)
    for CID in cid_set:
        cages[CID] = cage(CID)

    #Update remaining cage attributes from cage df
    for i in range(len(cdf_ls)):
        CID = str(cdf_ls[i])
        status = df_c['Status/Condition'][i]
        if not pd.isnull(status) and not str(status).isspace():
            cages[CID].color = conds[status][0]
            cages[CID].pri = conds[status][1]
        cages[key].pups = df_c['Number of Pups'][i]
        cages[key].DOB = df_c['Pup DOB'][i]
        cages[key].WD = df_c['Wean Date'][i]
    
    #Initalize all mouse objects
    m_ls = df_m['Mouse ID'].tolist()      #list of all mouse IDs
    for i in range(len(m_ls)):
        MID = str(m_ls[i])
        if MID not in mice.keys():
            new_mouse = mouse(MID)
            CID = str(c_ls[i])
            cages[CID].mice.append(MID)
            if str(df_m['Ear Tag?'][i]).lower() in ('n', 'no'):
                new_mouse.ET = False
            if str(df_m['Sex'][i]).lower() == 'm':     #False: Female, True: Male
                new_mouse.sex = True
            new_mouse.age = int(df_m['Age (days)'][i])
            if str(df_m['Pregnant?'][i]).lower() in ('y', 'yes'):
                new_mouse.pregnant = True
            new_mouse.sacked = str(df_m['Sacked Status: Potential (P), Sacked (S), Died (D)'][i]).lower() #Blank, potential for sack (p), already sacked (s), or died (d)
            if str(df_m['Genotyped?'][i]).lower() in ('y', 'yes'):
                new_mouse.genotyped = True
            if str(df_m['Runt?'][i]).lower() in ('y', 'yes'):
                new_mouse.runt = True
            new_mouse.DOD = str(df_m['Date of Death'][i])
            mice[MID] = new_mouse

    return mice, cages


def parse_data(filename):
    file = open(filename, 'rb')

    #No longer necessary to remove empty rows; Switch to openpyxl engine for reading? Move all this logic over to error detection functions?
    mice_data, cage_data = pd.read_excel(file, sheet_name = 'Mice', skiprows = 1, engine = 'xlrd'), pd.read_excel(file, sheet_name = 'Cages', skiprows = 1, engine = 'xlrd')

    #Construct and sort mice/cage objects
    return gen_objs(mice_data, cage_data)
