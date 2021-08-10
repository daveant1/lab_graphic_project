#Module that logs status messages or errors, including filename errors, parsing errors, execution timestamps, etc.
import sys

#STATUS

#Excel file successfully parsed
def st_parse(ts):
    print('Excel file parsed successfully: ', ts + 's')
    return

#Graphic successfully printed and saved
def st_graph(ts):
    print('Colony graphic saved successfully: ', ts + 's')
    return

#Colony data successfully written
def st_colony_data(ts):
    print('Colony stat file saved successfully: ', ts + 's')
    return

#Graphic generation process complete
def st_done():
    print('Graphic generation process complete!')
    return

#Autoorrected sheet name
def st_autosheet(old_val, new_val):
    print('SHEETNAME: Corrected sheet name', old_val, 'to name', new_val)
    return

#Autoorrected column header
def st_autoheader(old_val, new_val):
    print('HEADER: Corrected column header', old_val, 'to header', new_val)
    return

#Autocorrected cell value
def st_autocell(position, old_val, new_val, type):
    print('CELL: Corrected', type, 'cell at', position, 'from', old_val, 'to', new_val)
    return

#Stripped whitespace from cell value
def st_stripcell(position, type):
    print('CELL: Stripped whitespace from', type, 'cell at', position)
    return


#ERROR

#Failed to find sheet name
def err_autosheet(expect_name):
    print('ERROR: Could not find column header "' + expect_name + '"')
    sys.exit(0)

#Failed to find sheet name
def err_autoheader(expect_name):
    print('ERROR: Could not find column header "' + expect_name + '"')
    sys.exit(0)

#Failed to autocorrect cell or cell requires manual correction
def err_autocell(position, old_val, type):
    print('ERROR: Could not find a correction for', type, 'cell', '"' + position + '".', 'Value =', old_val)
    return

#Could not find corresponding color cell for condition cell
def err_cond_color(position, condition):
    print('ERROR: Color cell', '"' + position + '"', 'is blank or not a valid color for condition', condition)
    return

#General error when any part of cell correction fails
def err_autocell_gen(sheetname):
    print('ERROR: Cell autocorrection process failed for sheet "' + sheetname + '"')
    sys.exit(0)

#Filename error
def err_filename():
    print('ERROR: No file with name format <prefix>00-00-0000.xlsx found! (Example: prefix_of_file_00-00-0000.xlsx)')
    sys.exit(0)
    
#Unrecognized sheet name
def err_sheetname(sheetname):
    print('ERROR: Did not recognize sheet name', sheetname)
    sys.exit(0)

#Duplicate Cage IDs in Cages sheet
def err_dup_cid(cid):
    print('ERROR: Duplicate Cage ID for Cage "'+cid+'"')
    return

#Cage ID Missing from Cages sheet
def err_miss_cage(cid):
    print('ERROR: Missing cage; Cage ID"'+cid+'" is present in Mice sheet but not Cages sheet')
    return


#WARNING

#Chose default value for cell
def warn_autocell(position, old_val, new_val, type):
    print('WARNING: ' + type + ' cell "' + position + '" is blank or not recognized. Defaulting to', new_val)
    return

#Empty cages will be printed
def warn_empty_cage(cid):
    print('WARNING: Empty cage; Cage ID"'+cid+'" is present in Cages sheet but not Mice sheet')
    return