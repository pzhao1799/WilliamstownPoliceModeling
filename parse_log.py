import re
import pandas as pd
import numpy as np
filename = "./2019_low/out.txt"

file = open(filename, "r")
out = open("cleaned_out_2019_low.txt", "w")

def clean(text):
    # text = text.replace("", "")
    # text = text.replace("|", "")
    text = text.replace(";", ":")
    text = text.replace("~", "-")
    text = text.replace("--", "-")
    try:
        first_i = text.find(next(filter(str.isalnum, text)))
    except StopIteration:
        return ""
    
    return text[first_i:]

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
    out.write(e)
    out.write("\n")

df = pd.DataFrame(data=range(len(list_of_entries)-1),columns=['log']) #intentionally not including top output

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
    space = e.index(" ")
    return e[0:space]

def get_time(e):
    space1 = e.index(" ")
    space2 = e.index(" ",space1+1)
    return e[space1+1:space2]


def get_status(e):
    space1 = e.index(" ")
    space2 = e.index(" ",space1+1)
    end_of_line = e.index('\n')
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
    return e[start + incr:e.index(" ",start)]

logs = []
times = []
status = []
call_taker = []
location = []
unit = []
arvd = []
clrd = []

# for i in range(len(list_of_entries)):
#     e = list_of_entries[i]
#     if (e.find("20-") !=-1 and e.find("20-") < 3 ):
#         logs.append(get_log(e))
#         times.append(get_time(e))
#         status.append(get_status(e))
#         call_taker.append(get_title(e,"Call Taker:",2))
#         location.append(get_title(e,"Location/Address:",3))
#         unit.append(get_title(e,"Unit:",4))
#         arvd.append(get_arvd(e))
#         clrd.append(get_title(e,"Clrd-",5))
#         print(e.find("20-"))
#     print(e)

# df['log'] = logs
# df['time'] = times
# df['status'] = status
# df['call_taker'] = call_taker
# df['location'] = location
# #df['unit'] = unit
# #df['arvd'] = arvd
# #df['clrd'] = clrd
# print(df)

file.close()
out.close()
