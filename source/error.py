#Module that detects and autocorrects errors
import sys
import os
import re
import pygame
from openpyxl import load_workbook
from spellchecker import SpellChecker
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
        true_names = ['Mouse ID', 'Cage ID', 'Ear Tag?', 'Sex', 'DOB', 'Age (days)', 'Pregnant?', 'Sacked Status: Potential (P), Sacked (S), Died (D)', 'Date of Death', 'Genotyped?', 'Runt?', 'Comments']
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

#Mouse cell detection function; Iterates through selected columns and checks for blank cells
def detect_cells_m(worksheet):
    # Construct column headers dict (value:cell obj)
    headers = worksheet['2']
    col_dict = {h.value:h.column for h in headers if h.value is not None}
    failed = False     #bool to show when we have failed
    #Check Mouse IDs
    m_id_col = worksheet[col_dict['Mouse ID']][2:]      #Skip headers and blank cells
    for cell in m_id_col:
        if cell.value is None or str(cell.value).isspace():
            failed = True
            err_autocell(str(cell.column)+str(cell.row), cell.value, 'Mouse ID')       
    #Check Cage IDs
    c_id_col = worksheet[col_dict['Cage ID']][2:]
    for cell in c_id_col[2:]:
        if cell.value is None or str(cell.value).isspace():
            failed = True
            err_autocell(str(cell.column)+str(cell.row), cell.value, 'Cage ID')
    #Check Sex
    sex_col = worksheet[col_dict['Sex']][2:]
    for cell in sex_col:
        if str(cell.value).lower() not in ('f', 'm'):
            old_val = cell.value
            cell.value = 'F'
            warn_autocell(str(cell.column)+str(cell.row), old_val, cell.value, 'Sex')
    #Check Ages
    age_col = worksheet[col_dict['Age (days)']][2:]
    for cell in age_col:
        if cell.value is None or str(cell.value).isspace():
            old_val = cell.value
            cell.value = 0
            warn_autocell(str(cell.column)+str(cell.row), old_val, cell.value, 'Age')
        elif ' ' in str(cell.value):     #Check if contains whitespace
            cell.value.strip()
            st_stripcell(str(cell.column)+str(cell.row), 'Age')
    if failed:
        err_autocell_gen('Mice')
    return worksheet

#Cage cell detection function; Iterates through selected columns and checks for blank cells
def detect_cells_c(worksheet):
    # Construct column headers dict (value:cell obj)
    headers = worksheet['2']
    col_dict = {h.value:h.column for h in headers if h.value is not None}
    failed = False
    #Check Cage IDs
    c_id_col = worksheet[col_dict['Cage ID']][2:]
    for cell in c_id_col:
        if cell.value is None or str(cell.value).isspace():
            failed = True
            err_autocell(str(cell.column)+str(cell.row), cell.value, 'Cage ID')
    #Check condition/color chart
    cond_col = worksheet[col_dict['Condition']][2:]
    color_list = pygame.color.THECOLORS.keys()
    for cond_cell in cond_col:
        if cond_cell.value is not None and not str(cond_cell.value).isspace():
            pos = str(col_dict['Color']) + str(cond_cell.row)
            color = worksheet[pos].value
            if color is None or str(color).isspace() or color not in color_list:
                failed = True
                err_cond_color(pos, cond_cell.value)
    if failed:
        err_autocell_gen('Cages')
    return worksheet

#Function to simply delete the blank rows from the excel sheet to avoid confusion with blank cells
def delete_blank_rows(worksheet):
    for row in worksheet:
        if not any(cell.value for cell in row): #Row is completely blank
            worksheet.delete_rows(row[0].row)
    return worksheet

#Function to compare list of cages generated by mouse sheet and cage sheet
def compare_cage_lists(l1, l2):
    return

#Main error detection function: Calls subroutines for checking and correcting/logging sheet names, column headers, and cell values
def detect(filename):
    wb = load_workbook(filename)        #Load workbook
    wb = detect_sheetnames(wb)          
    ws_m = wb['Mice']                   #Load worksheets
    ws_c = wb['Cages']
    ws_m = delete_blank_rows(ws_m)      #Delete blank rows
    ws_c = delete_blank_rows(ws_c)
    ws_m = detect_headers(ws_m)
    ws_c = detect_headers(ws_c)
    ws_m = detect_cells_m(ws_m)
    ws_c = detect_cells_c(ws_c)
    wb.save('new.xlsx')                 #Save file

    sys.exit(0)


