import re
import pandas as pd
import numpy as np
import time
import sys
import argparse

def clean(text):
    # text = text.replace("", "")
    text = text.replace("|", "")
    text = text.replace(";", ":")
    text = text.replace("~", "-")
    text = text.replace("--", "-")
    text = re.sub(' +',' ',text)
    try:
        first_i = text.find(next(filter(str.isalnum, text)))
    except StopIteration:
        return ""
    
    return text[first_i:]

def get_EOL_n(e,n):
    counter = 1
    prev = 0
    while counter<10:
         current_line = e.find("\n",prev)
         if counter ==n:
             return current_line
         else:
             prev = current_line + 1
             counter+=1
    else:
        raise ValueError('No valid line found.')

def get_log(e):
    space = e.find(" ")
    return e[0:space]

def get_time(e):
    space1 = e.find(" ")
    space2 = e.find(" ",space1+1)
    return e[space1+1:space2]

def get_status(e):
    space1 = e.find(" ")
    space2 = e.find(" ",space1+1)
    end_of_line = e.find('\n')
    return e[space2+1:end_of_line]

# old
def OLD_get_title(e,title,line):
    start = e.find(title)
    incr = len(title)
    return e[start + incr:get_EOL_n(e,line)]

# TODO: Implement find_levenshtein function for finding strings within a certain Lev distance of a string. Should be usable given short length of entries, and incorporate into get_title

# Searches for text between a title and an ending token (endline character by default, and special option of None returns the whole rest of the source string starting at the title). Has verbose option that prints parameters and return value to console.
def get_title(e,title,end_token="\n",iter = False,verbose=False):
    search = re.search(title,e)
    # If we can't find the string, return "N/A".
    if iter ==True: #used for multiple iterations such as clrd,arvd. 
        string = ""
        for m in re.finditer(title, e):
            end = m.end()
            search_end_token = re.search(end_token,e[end:])
            print(e[end : search_end_token.start() + end])
            if search_end_token ==None:
                string = string + ";N/A"
            else:
                string = string + ";" + e[end : search_end_token.start() + end]
        return string[1:] #remove first ; to make formatting consistant

    if search == None:
        if verbose:
            print("Failed to find text between string " + repr(title) + " and string " + repr(end_token) + ".")
        return "N/A"
    start = search.start()
    end = search.end()
    incr = end - start
    # Using special option None for end_token returns the whole rest of the string.
    if end_token == None:
        if verbose:
            print("Failed to find text between string " + repr(title) + " and string " + repr(end_token) + ".")
        return e[end:].replace("Narrative:", ";") #strips off for extra additions
    search_end_token = re.search(end_token,e[end:])
    # If we can't find the ending token, return "N/A".
    if search_end_token == None:
        if verbose:
            print("Failed to find text between string " + repr(title) + " and string " + repr(end_token) + ".")
        return "N/A"
    if verbose:
        print("Found text between string " + repr(title) + " and string " + repr(end_token) + ": " + repr(e[end : search_end_token.start() + end]))
    if end_token == "Sex:":
        return e[end : search_end_token.start() + end + 6] #janky way of accounting for extra line
    # Return the substring between the end of the title and the beginning of the end token.
    return e[end : search_end_token.start() + end]

########## Run ##########

# Create the parser
parser = argparse.ArgumentParser(description='OCR')

# Add the arguments
parser.add_argument('input',
                    metavar='input',
                    type=str,
                    help='the path to input')
parser.add_argument('output',
                    metavar='output',
                    type=str,
                    help='the path to out')

args = parser.parse_args()

time_1 = time.time()
in_filename = args.input
out_filename = args.output

# Open read and write files
in_file = open(in_filename, "r", encoding="utf8") # the uncleaned text file we read in
# text_out = open(out_filename, "w", encoding="utf8") # the cleaned text file (output)

# Turn source text file into list of entries.
list_of_entries = []
temp = ""
for line in in_file:
    line = clean(line)
    if re.match("[0-9]+[-][0-9]+\s", line):
        list_of_entries.append(temp)
        temp = ""
    temp += line

# # Write cleaned list of entries to new text file.
# for e in list_of_entries:
#     text_out.write(e)
#     text_out.write("\n")

# Initialize database.
df = pd.DataFrame(data=range(len(list_of_entries)-1),columns=['log']) #intentionally not including top output
df_entries = []
df_columns = ['log','time','status','call_taker','location','unit', 'disp', 'enrt','arvd','clrd','narrative','vehicle', 'citation', 'operator', 'owner']

# Add entries to database.
for i in range(len(list_of_entries)):
     e = list_of_entries[i]
     current = []
     if "-" in get_log(e):
         current.append(get_log(e))
         current.append(get_time(e))
         current.append(get_status(e))
         current.append(get_title(e,"Call Taker: "))
         current.append(get_title(e,"Location/Address: "))
         current.append(get_title(e,"Unit: ", iter=True))
         #current.append(get_title(e,"A.?r.?v.?d.?.?-"," C.?l.?r.?d.?.?-")) #was breaking with multiple iterations
         #current.append(get_title(e,"C.?l.?r.?d.?.?-"))
         current.append(get_title(e,"Disp-", " ", iter=True))
         current.append(get_title(e,"Enrt-", " ", iter=True))
         current.append(get_title(e,"Arvd-", " ", iter=True))
         current.append(get_title(e,"Clrd-", iter=True))
         current.append(get_title(e,"Narrative:\n",None))
         current.append(get_title(e,"Vehicle: "))
         current.append(get_title(e,"Refer To Citation: "))
         current.append(get_title(e,"Operator: ", "Sex:"))
         current.append(get_title(e,"Owner: ", "Sex:"))
         df_entries.append(current)
print("Added",i,"entries to list.")

in_file.close()
# text_out.close()

# Export database to csv for easy viewing/interaction. This is the point where we'll move to the next step in the data pipeline.
csv_out = out_filename # the location where we'll write a csv file
print("Converting list to dataframe...")
df = pd.DataFrame(df_entries,columns=df_columns)
print("Exporting CSV...")
df.to_csv(csv_out,sep=",")

time_2 = time.time()
print("Done: " + str(time_2 - time_1) + " seconds.")
