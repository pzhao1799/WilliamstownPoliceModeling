import re
filename = "./test/out.txt"

file = open(filename, "r")

def clean(text):
    # text = text.replace("", "")
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

for e in list_of_entries:
    print("################################################")
    print(e)


file.close()