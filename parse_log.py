import re
import pandas as pd
import numpy as np

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

def get_title(e,title,line):
    start = e.find(title)
    incr = len(title)
    return e[start + incr:get_EOL_n(e,line)]
    
def get_arvd(e):
    search = re.search("A.?r.?v.?d.?.?-",e)
    if search != None:
        start = search.start()
    else:
        return "N/A"
    incr = len("Arvd-")
    return e[start + incr:e.find(" ",start)]

########## Run ##########

#####
file = open("./2019_low/out.txt", "r", encoding="utf8") # the uncleaned text file we read in
text_out = open("cleaned_out_2019_low.txt", "w", encoding="utf8") # the cleaned text file (output)
csv_out = "2019_low.csv" # the location where we'll write a csv file
#####

list_of_entries = []
temp = ""
for line in file:
    line = clean(line)
    # templine = line.replace(" ", "")
    if re.match("[0-9]+[-][0-9]+\s", line):
        list_of_entries.append(temp)
        temp = ""
    temp += line

for e in list_of_entries:
    text_out.write(e)
    text_out.write("\n")

df = pd.DataFrame(data=range(len(list_of_entries)-1),columns=['log']) #intentionally not including top output
df_entries = []

for i in range(len(list_of_entries)):
     e = list_of_entries[i]
     current = []
     if "-" in get_log(e):#(e.find("20-") !=-1 and e.find("20-") < 3 ):
         current.append(get_log(e))
         current.append(get_time(e))
         current.append(get_status(e))
         current.append(get_title(e,"Call Taker:",2))
         current.append(get_title(e,"Location/Address:",3))
         current.append(get_title(e,"Unit:",4))
         current.append(get_arvd(e))
         current.append(get_title(e,"Clrd-",5))
         df_entries.append(current)
     if i % 1000 == 0:
         print("Added",i,"entries to list.")

print("Converting list to dataframe...")
df = pd.DataFrame(df_entries,columns=['log','time','status','call_taker','location','unit','arvd','clrd'])
# The DataFrame is pretty big for displaying the whole thing in IDE, so I shifted to expoting to csv.
print("Exporting CSV...")
df.to_csv(csv_out,sep=",")
print("Done.")

file.close()
text_out.close()
