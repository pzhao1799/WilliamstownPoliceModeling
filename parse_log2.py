import re
import pandas as pd
import numpy as np
filename = "./test/out.txt"
file = open(filename, "r")

def clean(text):
    # text = text.replace("", "")
    # text = text.replace("|", "")
    text = text.replace(";", ":")
    text = text.replace("~", "-")
    try:
        first_i = text.find(next(filter(str.isalnum, text)))
    except StopIteration:
        return ""

    return text[first_i:]


list_of_entries = []
temp = ""
for line in file:
    line = clean(line)
    if line.startswith("20-"):
        list_of_entries.append(temp)
        temp = ""
    temp += line


df = pd.DataFrame(data=range(len(list_of_entries)),columns=['log'])

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

logs = []
times = []
status = []

for i in range(len(list_of_entries)):
    e = list_of_entries[i]
    logs.append(get_log(e))
    times.append(get_time(e))
    status.append(get_status(e))
    print(e)

df['log'] = logs
df['time'] = times
df['status'] = status
print(df)

file.close()