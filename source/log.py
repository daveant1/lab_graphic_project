#Module that logs status messages or errors, including filename errors, parsing errors, execution timestamps, etc.

#STATUS

#Excel file successfully parsed
def st_parse(ts):
    print('Excel file parsed successfully: ', ts + 's')

#Graphic successfully printed and saved
def st_graph(ts):
    print('Colony graphic saved successfully: ', ts + 's')

#Colony data successfully written
def st_coldata(ts):
    print('Colony stat file saved successfully: ', ts + 's')

#Graphic generation process complete
def st_done():
    print('Graphic generation process complete!')


#ERROR

#Filename error
def err_filename():
    print('Error: No file with name format <prefix>00-00-0000.xlsx found! (Example: prefix_to_file_00-00-0000.xlsx)')

#Next error
def next_error():
    return
