## Documentation
This file explains the design and usage of the tools provided in this repository.

## Design
The main files that are used are `ocr.py`, `clean.py`, `parse_log.py`, and `interactive_map.py`.

The `ocr.py` file contains all the necessary functions to perform optical character recognition, and convery a batch set of PDFs to a text file. As input, it takes in
a directory of PDF files, a directory for the images produced per page of the PDF, and an output text file. The reason we store all of the images produced locally is so
that if a user has enormous amount of PDF files, they can store the intermediate stage without having the restart the process if the system crashes in the middle. The
OCR process also utilizes the `clean.py` file, which gets rid of any redactions if the documents contain any so that redactions can be recognized separately. The OCR of
each PDF uses the Tesseract OCR Engine, which is an open source engine that can be used for easily performing OCR. There are various modes for running this file, so that
you may complete each step separately (PDF to Image and Image to Text), or run them all at once. The functions also provide a parameter for ordering the PDFs if you want
to order the output in a specified format. Otherwise, the default file system ordering is used.

The functions in `interactive_map.py` were designed to be used alongside `parse_log.py`, but may still be useful as standalone functions. The main functions of value are make_map(df), which takes in a dataframe consisting of the whole dataset and saves a folium map into the directory of the program, and make_loc_circle_map(df), which takes in a dataframe consisting of a modified version of the dataset that contains the unique location and counts of logs with those locations. Both of the types of dataframes needed correspond to worksheets in 'combined_output_updated.xlsx', those being 'data' and 'location'

Even though the code for doing so has not been provided in our repo, all one would need to do to use this function in another program is to have the line `df = pd.read_excel('SampleWork.xlsx', sheet_name = 'this_sheet')` right before the corresponding function call, and then a map will be saved in their repo. 
