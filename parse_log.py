import re
filename = "./high_res/out_file.txt"

file = open(filename, "r")
out = open("cleaned_out.txt", "w")

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
        print(line)
        list_of_entries.append(temp)
        temp = ""
    temp += line

for e in list_of_entries:
    out.write(e)
    out.write("\n")


file.close()
out.close()