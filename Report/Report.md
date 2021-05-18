# Final Report

### Goals/Motivations

### Materials

### Process

### Current State of Things
Currently, we have developed a small set of Python scripts that assist in the processing
of the multiple files in a pipelined fashion. We decided that there were a few separable steps
in which we could interpret our data, and we list them below.

1. Paper to PDF Scanning
2. PDF to Text via OCR
3. Text Cleaning
4. Analysis

First, we scanned in all the physical documents we had for parsing. Then, we utilized the 
Tesseract Open Source OCR Engine to convert all PDFs we had into a text file that we could 
manipulate in code. Since the OCR results were not very clean, we needed another script that 
would clean the text, removing characters that were incorrect and fixing characters that had 
been interpreted incorrectly. These fixes were first identified manually, and then reparied 
using regular expressions and pattern matching. Then, this raw data text was converted into
a Pandas Dataframe so that we could more easily manipulate it. After the dataframe was created,
we were able to perform analysis, such as mapping out the locations, utilizing fuzzy pattern 
matching to search for keywords, and performing elementary data analysis.

### Next Steps
