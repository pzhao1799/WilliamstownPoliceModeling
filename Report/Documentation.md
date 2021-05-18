## Documentation
This file explains the design and usage of the tools provided in this repository.

## Design
The main files that are used are `ocr.py`, `clean.py`, `parse_log.py`, and `interactive_map.py`.
In order to use these files, 

The functions in `interactive_map.py` were designed to be used alongside `parse_log.py`, but may still be useful as standalone functions. The main functions of value are make_map(df), which takes in a dataframe consisting of the whole dataset and saves a folium map into the directory of the program, and make_loc_circle_map(df), which takes in a dataframe consisting of a modified version of the dataset that contains the unique location and counts of logs with those locations. Both of the types of dataframes needed correspond to worksheets in 'combined_output_updated.xlsx', those being 'data' and 'location'

Even though the code for doing so has not been provided in our repo, all one would need to do to use this function in another program is to have the line `df = pd.read_excel('SampleWork.xlsx', sheet_name = 'this_sheet')` right before the corresponding function call, and then a map will be saved in their repo. 
