#Module that logs status messages or errors, including filename errors, parsing errors, execution timestamps, etc.
import sys

#STATUS

#Begin detect() function
def st_detect():
    print('SHEET DETECTION:\n')
    return

#Excel file successfully parsed
def st_parse(ts):
    print('\n\nGRAPHIC GENERATION:\n')
    print('Excel file parsed successfully: ', str(ts)+'s\n')
    return

#Graphic successfully printed and saved
def st_graph(ts):
    print('Colony graphic saved successfully: ', str(ts)+'s\n')
    return

#Colony data successfully written
def st_colony_data(ts):
    print('Colony stat file saved successfully: ', str(ts)+'s\n')
    return

#Graphic generation process complete
def st_done():
    print('Graphic generation process complete!')
    return

#Autoorrected sheet name
def st_autosheet(old_val, new_val):
    print('SHEETNAME: Corrected sheet name "'+str(old_val)+'" to name "'+str(new_val)+'"\n')
    return
    
#Autoorrected column header
def st_autoheader(old_val, new_val):
    print('HEADER: Corrected column header "'+str(old_val)+'" to header "'+str(new_val)+'"\n')
    return

#Autocorrected cell value
def st_autocell(position, old_val, new_val, type):
    print('CELL: Corrected', type, 'cell at', position, 'from "'+str(old_val)+'" to "'+str(new_val)+'"\n')
    return

#Deleted blank rows
def st_del_rows(row_diff, sheetname):
    print('ROW: Deleted', row_diff, 'blank rows from '+sheetname+' sheet\n')
    return

#Error/warn/fix count message
def st_ewf(ewf):
    print('Total Errors:', ewf[0], ' Total Warnings:', ewf[1], ' Total Fixes:', ewf[2])
    return


#ERROR

#Failed to find sheet name
def err_autosheet(expect_name, ewf):
    print('FATAL ERROR: Could not find sheet name "'+expect_name+'"\n')
    st_ewf(ewf)
    sys.exit(0)

#Failed to find column header
def err_autoheader(expect_name):
    print('ERROR: Could not find column header "'+expect_name+'"\n')
    return

#Failed to autocorrect cell or cell requires manual correction
def err_autocell(position, old_val, type):
    print('ERROR: Could not find a correction for', type, 'cell at '+position+'.', 'Value = "'+str(old_val)+'"\n')
    return

#Could not find corresponding color cell for condition cell
def err_cond_color(position, color):
    print('ERROR: Color cell at '+position+' is blank or not a valid X11 color. Value = "'+str(color)+'"\n')
    return

#General error when any part of cell correction fails
def err_autocell_gen(sheetname, ewf):
    print('FATAL ERROR: Cell autocorrection process failed for '+sheetname+' sheet\n')
    st_ewf(ewf)
    sys.exit(0)

#Filename error
def err_filename(ewf):
    print('FATAL ERROR: No file with name format <prefix>00-00-0000.xlsx found! (Example: prefix_of_file_00-00-0000.xlsx)\n')
    st_ewf(ewf)
    sys.exit(0)

#Duplicate Cage IDs in Cages sheet
def err_dup_cid(cid):
    print('ERROR: Duplicate Cage ID "'+str(cid)+'" from Cages sheet\n')
    return

#Cage ID Missing from Cages sheet
def err_miss_cage(cid):
    print('ERROR: Missing cage. Cage ID "'+str(cid)+'" is present in Mice sheet but not Cages sheet\n')
    return


#WARNING

#Chose default value for cell
def warn_autocell(position, old_val, new_val, type):
    print('WARNING: '+type+' cell at '+position+' is blank or not recognized. Value = "'+str(old_val)+'".', 'Defaulting to "'+str(new_val)+'"\n')
    return

#Empty cages will be printed
def warn_empty_cage(cid):
    print('WARNING: Empty cage. Cage ID "'+str(cid)+'" is present in Cages sheet but not Mice sheet\n')
    return
