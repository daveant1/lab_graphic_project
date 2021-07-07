#Module that detects and autocorrects errors
import sys
import os
import re
from openpyxl import load_workbook
from spellchecker import SpellChecker
import json
from log import *

#Function to search for and parse filename with regex
def parse_filename():
    dir = os.listdir(os.getcwd())
    #Check for valid excel file
    for file in dir:
        match = re.search(r'(\w*)(\d\d\-\d\d\-\d+)(\.xlsx)', file)     #Filename is "<Alphanumeric and _>00-00-0*.xlsx"
        if match != None:
            break
    if match == None:
        err_filename()
    filename = match.group(0)
    return match, filename

#Subroutine of detect() that checks sheetnames
def detect_sheetnames(workbook):
    #TODO: create dict(s) manually in code rather than introducing additional json files
    sp = SpellChecker(language=None, distance=3, case_sensitive=True)
    true_names = ['Mice', 'Cages']
    for name in true_names:
        sp.word_frequency.add(name)
    for word in sp.unknown(workbook.sheetnames):
        new_name = sp.correction(word)
        if new_name is not word:                    #Make sure correction found
            workbook[word].title = new_name
            st_autosheet(word, new_name)           #Log change to sheet name
    #Check if expected sheetnames all present
    for name in true_names:
        if name not in workbook.sheetnames:
            err_autosheet(name)
    return workbook

#Subroutine of detect() that checks column headers
def detect_headers(worksheet):
    if worksheet.title == 'Mice':
        true_names = ['Mouse ID', 'Cage ID', 'Ear Tag?', 'Sex', 'DOB', 'Age (days)', 'Pregnant?', 'Sacked Status: Potential (P), Sacked (S), Sacrificed (D)', 'Date of Death', 'Genotyped?', 'Runt?', 'Comments']
    elif worksheet.title == 'Cages':
        true_names = ['Cage ID', 'Status/Condition', 'Number of Pups', 'Pup DOB', 'Wean Date', 'Condition', 'Color']
    else: 
        err_sheetname(worksheet.title)
    sp = SpellChecker(language=None, distance=3, case_sensitive=True)
    for name in true_names:
        sp.word_frequency.add(name)
    headers = worksheet['2']
    head_hash = {h.value:str(h.column)+str(h.row) for h in headers if h.value is not None}   #Generate hash of header:position
    for word in sp.unknown(head_hash.keys()):
        new_name = sp.correction(word)
        if new_name is not word:                    #Make sure correction found
            cell = worksheet[head_hash[word]]       #Select cell with incorrect word
            cell.value = new_name
            st_autoheader(word, new_name)           #Log change to column header
    #Create list of current headers after autocorrection process
    curr_headers = [h.value for h in headers if h.value is not None]
    #Check if expected headers all present
    for name in true_names:
        if name not in curr_headers:
            err_autoheader(name)
    return worksheet

#Subroutine of detect() to check blank or whitespace cells
def detect_cells(worksheet):
    print(worksheet.max_column)
    print(worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, max_col=worksheet.max_column))
    for i in range(1, worksheet.max_column+1):
        worksheet[1]
    # worksheet.iter_rows(min_row)
    # position, old_val, new_val = ''
    # st_autocell(position, old_val, new_val)
    # return worksheet

#Main error detection function: Calls subroutines for checking and correcting/logging sheet names, column headers, and cell values
def detect(filename):
    wb = load_workbook(filename)        #Load workbook
    wb = detect_sheetnames(wb)          
    ws_m = wb['Mice']                   #Load worksheets
    ws_c = wb['Cages']
    ws_m = detect_headers(ws_m)
    ws_c = detect_headers(ws_c)
    # ws_m = detect_cells(ws_m)
    # ws_c = detect_cells(ws_c)
    wb.save('new.xlsx')                 #Save file

    sys.exit(0)


