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
    sp = SpellChecker(language=None, local_dictionary='sheetname_dict.json', distance=3, case_sensitive=True)
    for word in sp.unknown(workbook.sheetnames):
        new_name = sp.correction(word)
        if new_name is not word:                    #Make sure correction found
            workbook[word].title = new_name
            st_autosheet(word, new_name)           #Log change to sheet name
    with open('sheetname_dict.json') as f:
        data = json.loads(f.read())
    for key in data.keys():
        if key not in workbook.sheetnames:
            err_autosheet(key)
    return workbook

#Subroutine of detect() that checks column headers
def detect_headers(worksheet, dict_path):
    sp = SpellChecker(language=None, local_dictionary=dict_path, distance=3, case_sensitive=True)
    headers = worksheet['2']
    head_hash = {h.value:str(h.column)+str(h.row) for h in headers if h.value is not None}   #Generate hash of header:position
    for word in sp.unknown(head_hash.keys()):
        cell = worksheet[head_hash[word]]       #Select cell with incorrect word
        new_name = sp.correction(word)
        if new_name is not word:                    #Make sure correction found
            cell.value = new_name
            st_autoheader(word, new_name)           #Log change to column header
    #Create list of current headers
    curr_headers = []
    for h in headers:
        curr_headers.append(h.value)
    #Check if expected headers all present
    with open(dict_path) as f:
        data = json.loads(f.read())
    for key in data.keys():
        if key not in curr_headers:
            err_autoheader(key)
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
    ws_m = detect_headers(ws_m, 'header_dict_m.json')
    ws_c = detect_headers(ws_c, 'header_dict_c.json')
    # ws_m = detect_cells(ws_m)
    # ws_c = detect_cells(ws_c)
    # wb.save('new.xlsx')                 #Save file

    sys.exit(0)


