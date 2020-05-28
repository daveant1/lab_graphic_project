import pandas as pd
import re
from objects import *

#Input: pandas data frame from colony_data
#Output: Vector of mouse objects and vector of cage objects
def gen_objs(df):
    mice = []      #empty vector of mouse objects
    cages = []     #empty vector of cage objects
    col_list = df.columns.tolist()

#Construct and assign mouse vectors to cages
    c_ls = df['Cage ID'].tolist()      #list of all cages including repeats
    m_ls = df['Mouse ID'].tolist()      #list of all mouse IDs

    #Loop to generate new cage based on new Cage ID
    #print(c_ls)
    prev_cage = c_ls[0]
    new_cage = cage(str(c_ls[0]))
    self_mice = []
    for i in range(len(c_ls)):
        if c_ls[i] != prev_cage:
            new_cage.mice = self_mice
            new_cage.total = len(self_mice)
            cages.append(new_cage)
            new_cage = cage(str(c_ls[i]))
            self_mice = []      #vector of mice specific to one cage
            prev_cage = str(c_ls[i])

        self_mice.append(str(m_ls[i]))

    #set members and append again for final cage outside loop
    new_cage.mice = self_mice
    new_cage.total = len(self_mice)
    cages.append(new_cage)
    #for c in cages:
        #print(c.CID)

    #Loop to initalize all mice objects
    for i in range(len(m_ls)):
        new_mouse = mouse(str(m_ls[i]))
        new_mouse.CID = str(c_ls[i])
        if df['Ear Tag?'][i] == 'No':
            new_mouse.ET = False
        if df['Sex'][i] == 'M':     #False: Female, True: Male
            new_mouse.sex = True
        new_mouse.age = df['Age (days)'][i]
        if df['Pregnant?'][i] == 'Yes':
            new_mouse.pregnant = True
        new_mouse.sacked = df['Sacked Status (Blank, Potential, Sacked)'][i]   #Blank, may be sacked (Potential), or already sacked (Sacked)
        new_mouse.DOS = df['Date of Sack'][i]
        if df['Genotyped?'][i] == 'Yes':
            new_mouse.genotyped = True
        if df['Runt?'][i] == 'Yes':
            new_mouse.runt = True
        new_mouse.comment = df['Comments'][i] #Comment entry
        mice.append(new_mouse)
    #print(len(mice),len(cages))
    return mice, cages

#This function fills in the remaining info for the cage objects from the second excel sheet
#Input: pandas data frame of cages sheet, unfinished vector of cages
#Output: finished vector of cages
def finish_cages(df, cages):
    for i in range(len(cages)):
        if df['Breeding?'][i] == 'Yes':
            cages[i].breeding = True
        cages[i].EC = df['Experimental Condition'][i]
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
    # for m in mice:
    #     print(vars(m))
    return mice, final_cages
