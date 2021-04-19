# How to search fuzzy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas
import argparse
import sys
import math

# Create the parser
parser = argparse.ArgumentParser(description='OCR')

# Add the arguments
parser.add_argument('csv',
                    metavar='csv',
                    type=str,
                    help='the path to input')

args = parser.parse_args()

df = pandas.read_csv(args.csv)


while True:
    column = input("Column name to search: ").lower()
    searchterm = input("Search string: ").lower()
    for i, entry in enumerate(df[column]):
        if isinstance(entry, str) and fuzz.ratio(searchterm, entry.lower()) > 80:
            print("Row " + str(i) + " " + entry)
            #print(df.iloc[[i]])

