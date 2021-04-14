# Williamstown Police Modeling
## Math Modeling Spring 2021
Authors: Peter Zhao, Andrew Thai, Spencer Brooks, Joshua Hewson, Porter Johnson

## Requirements
- python 3+
- pip
- pdf2image
    - poppler
- pytesseract
    - tesseract
- PILLOW
- pandas
- numpy

```
$ pip install pdf2image
$ pip install pytesseract
$ pip install Pillow
$ pip install pandas
$ pip install numpy
```

Ubuntu (Linux) Only:
```
$ sudo apt-get install poppler-utils
$ sudo apt-get install tesseract-ocr
```

MacOS Only:
```
$ brew install poppler
```

Todo: Need an easier way to install poppler for Windows.

## How to Run

### OCR:

```
py ./ocr.py pdf-path png-path outfile mode
```

- `pdf-path` is the path to the directory containing the pdf files.

- `png-path` is the path to the directory containing the png files OR where the png files will be created when converting from the pdfs.

- `outfile` is the name of the file that will contain the resulting text.

- `mode` is the type of conversion to be done.
    - `"pdf"` will only convert the pdfs to pngs.
    - `"ocr"` will only convert the pngs to text.
    - `"both"` will do the full conversion from pdfs to text.

### Text Cleanup and Parsing:

```
$ py ./parse_log.py
```

TODO: parse_log.py currently has a global variable with the text file to parse and clean. It should be changed to take in a command line argument with the text file we want to edit.