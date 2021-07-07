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

#Autoorrected cell value
def st_autocell(position, old_val, new_val):
    print('CELL: Corrected cell', position, 'from', old_val, 'to', new_val)
    return

#ERROR

#Failed to find sheet name
def err_autosheet(expect_name):
    print('ERROR: Could not find sheet', '"'+expect_name+'"')
    sys.exit(0)

#Failed to find sheet name
def err_autoheader(expect_name):
    print('ERROR: Could not find column header', '"'+expect_name+'"')
    sys.exit(0)

#Autoorrected cell value
def err_autocell(position, old_val, new_val):
    print('WARNING: Could not find a correction for cell', '"'+position+'"')
    return

#Filename error
def err_filename():
    print('ERROR: No file with name format <prefix>00-00-0000.xlsx found! (Example: prefix_of_file_00-00-0000.xlsx)')
    sys.exit(0)
    
#Unrecognized sheet name
def err_sheetname(sheetname):
    print('ERROR: Did not recognize sheet name', sheetname)
    sys.exit(0)
    