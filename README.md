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
- fuzzywuzzy
- python-Levenshtein
- sqlalchemy

```
$ pip install pdf2image
$ pip install pytesseract
$ pip install Pillow
$ pip install pandas
$ pip install numpy
$ pip install fuzzywuzzy
$ pip install python-Levenshtein
$ pip install sqlalchemy
$ pip install folium
$ pip install geopy
```

Ubuntu (Linux) Only:
```
$ sudo apt-get install poppler-utils
$ sudo apt-get install tesseract-ocr
```

MacOS Only:
```
$ brew install poppler
$ brew install tesseract
```

Todo: Need an easier way to install poppler for Windows.

## How to Run

### OCR (ocr.py):

```
$ py ./ocr.py pdf-path png-path outfile mode
```

- `pdf-path` is the path to the directory containing the pdf files.

- `png-path` is the path to the directory containing the png files OR where the png files will be created when converting from the pdfs.

- `outfile` is the name of the file that will contain the resulting text.

- `mode` is the type of conversion to be done.
    - `"pdf"` will only convert the pdfs to pngs.
    - `"redact"` will only clean redaction marks on the pngs and output pngs.
    - `"ocr"` will only convert the pngs to text.
    - `"all"` will do the full conversion from pdfs to text.

### Text Cleanup and Parsing (parse_log.py):

```
$ py ./parse_log.py infile outfile
```

- `infile` is the path to the file containing the raw OCR output.

- `outfile` is the name of the file that will contain the cleaned text.

- The program currently always writes to a csv called `2019_low.csv`. This functionality will later be removed or changed.

### Building Maps (interactive_map.py):
- used in parse_log.py to create folium maps of the data.
- contains the function `geolocate` which was necessary for collection GPS data for maps
- has a secondary map generator `make_loc_circle_map` that is used to make bubble maps of occurrences (explained in readme)
- generates a map called `interactive_map.html`

## Next Steps
- https://policescorecard.org/
