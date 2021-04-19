from pandas import read_csv
from sqlalchemy import create_engine
import sys
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='SQL')

# Add the arguments
parser.add_argument('csv',
                    metavar='csv',
                    type=str,
                    help='the path to csv')

args = parser.parse_args()
df = read_csv(args.csv)

engine = create_engine('sqlite:///police_data.db', echo=True)
sqlite_connection = engine.connect()

df.to_sql(args.csv, sqlite_connection, if_exists='fail')

sqlite_connection.close()