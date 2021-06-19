#Module that detects and autocorrects errors
import sys
import os
import re
from log import *

#Function to search for and parse filename with regex
def parse_filename():
    dir = os.listdir(os.getcwd())
    #Check for valid excel file
    for file in dir:
        match = re.search(r'(\w*)(\d\d\-\d\d\-\d+)(\.xlsx)', file)     # filename is "<Alphanumeric and _>00-00-0*.xlsx"
        if match != None:
            break
    if match == None:
        err_filename()
        sys.exit(0)
    filename = match.group(0)
    return match, filename

#Function to loop through cells and check for blanks/spaces