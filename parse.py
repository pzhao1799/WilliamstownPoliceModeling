import re
filename = "./test/out.txt"

file = open(filename, "r")

"""
list_of_entries = [ ]
for line in file:
      if line contains regex:
            split at regex
            add the stuff before regex to current entry
            add entry to list_of_entries
            new entry
            add stuff after regex to current entry
      else:
            add line to current entry

"""
# s = "|$***^%*$$$## 1abc"
# i = s.find(next(filter(str.isalnum, s)))
# print(s[i:])

def clean(text):
    # text = text.replace("", "")
    # text = text.replace("|", "")
    try:
        first_i = text.find(next(filter(str.isalnum, text)))
    except StopIteration:
        return ""
    
    # print(text[first_i:])
    return text[first_i:]

list_of_entries = []
temp = ""
for line in file:
    line = clean(line)
    if line.startswith("20-"):
        list_of_entries.append(temp)
        temp = ""
    temp += line

for e in list_of_entries:
    print("################################################")
    print(e)


file.close()