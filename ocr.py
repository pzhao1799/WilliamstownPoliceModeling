import argparse
import os
import sys
import pdf2image as pdf
import pytesseract as pt
from PIL import Image
import numpy as np

from clean import Cleaner


# Dependencies
# pip3 install pytesseract, Pillow, pdf2image, scikit-image, numpy
# sudo apt-get install tesseract-ocr, poppler-utils

def pdf_to_images(pdf_path, png_path, offset):
    """
    Takes in a path pdf_path to a PDF file, and saves them in another directory of 
    png images numbered with offset.
    """
    pages = pdf.convert_from_path(pdf_path, dpi = 400)
    print("Finished pdf to image page generation")
    for page in pages:
        image_name = png_path + "/page_" + str(offset) + ".png"  
        offset+=1
        page.save(image_name, "PNG")
        print("Finished page to image conversion...")
    
    return offset
    
def redact(png_path):
    """
    Takes in a path png_path to a path of an image file, and overwrites it as a cleaned image file
    """
    file = Image.open(png_path)
    imarray = np.array(file)
    clean_array = Cleaner.find_redactions(imarray)
    file = Image.fromarray(clean_array)
    file.save(png_path, 'PNG')
    return
    

def ocr(png_path, fp):
    """
    Takes in a path png_path to a path of an image file, and appends to the file specified by
    fp
    """
    # TODO FIX
    image_file = Image.open(png_path)
    image_file = image_file.convert('L') # convert image to monochrome
    image_file = image_file.convert('1') # convert image to black and white 
    text = str(((pt.image_to_string(image_file, config='--psm 6 -c preserve_interword_spaces=1'))))
    fp.write(text)


def sort_directory(path, fn):
    return sorted(os.scandir(path), key = fn)

def directory_apply_pdf2images(pdf_path, png_path, sort):
    """
    Iterates through each file in the directory specified by dir_path, and applies the given function
    to each file, if each file is file_type.
    """
    offset = 1
    dir_entries = dir_entries = sort_directory(pdf_path, lambda x: int(x.path[x.path.rindex("-")+1:x.path.index(".")])) if sort else os.scandir(pdf_path)
    for entry in dir_entries:
        if (entry.path.endswith(".pdf") and entry.is_file()):
            print("!: " + entry.path)
            offset = pdf_to_images(entry.path, png_path, offset)
    print("PDF to Image conversion complete")
            
def directory_apply_redact(png_path):
    dir_entries = sort_directory(png_path, lambda x: int(x.path[x.path.rindex("/") + 6:x.path.index(".")]))
    for i, entry in enumerate(dir_entries):
        if (entry.path.endswith(".png") and entry.is_file()):
            redact(entry.path)
            print("Redacted page " + str(i) + "...")

def directory_apply_ocr(png_path, output, sort):
    """
    Iterates through each file in the directory specified by dir_path, and applies the given function
    to each file, if each file is file_type. Appends to output.
    """
    fp = open(output, "w")
    dir_entries = dir_entries = sorted(os.scandir(png_path), key = lambda x: int(x.path[x.path.rindex("/") + 6:x.path.index(".")])) if sort else os.scandir(png_path)
    for i, entry in enumerate(dir_entries):
        if (entry.path.endswith(".png") and entry.is_file()):
            ocr(entry.path, fp)
            print("OCR'd page " + str(i) +  "...")
    fp.close()
    print("OCR complete.") 


if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description='OCR')

    # Add the arguments
    parser.add_argument('pdfpath',
                        metavar='pdfpath',
                        type=str,
                        help='the path to pdf directory')
    parser.add_argument('pngpath',
                        metavar='pngpath',
                        type=str,
                        help='the path to png directory')
    parser.add_argument('outfile',
                        metavar='outfile',
                        type=str,
                        help='the output file')
    parser.add_argument('mode',
                        metavar='mode',
                        type=str,
                        help='the usage mode')
    parser.add_argument('sort',
                        metavar='sort',
                        type=int,
                        help='the sorting method',
                        default = 0)
                        

    args = parser.parse_args()

    pngs = os.listdir(args.pngpath)

    if args.mode == "test":
        # print(list(map(lambda x: int(x[3:x.index("_")]), os.listdir(args.pdfpath))))
        # sl = sorted(os.listdir(args.pdfpath), key = lambda x: int(x[x.index("-")+1:x.index("_")]))
        # for e in sl:
        #     print(e)
        pp = sorted(os.scandir(args.pdfpath), key = lambda x: int(x.path[x.path.rindex("-")+1:x.path.index(".")]))
        for i in pp:
            print(i)

    # Need to convert pdfs to pngs
    if args.mode == "pdf":
        directory_apply_pdf2images(args.pdfpath, args.pngpath, args.sort)
        pngs = os.listdir(args.pngpath)

    # Need to convert pngs to cleaned pngs
    if args.mode == "redact":
        directory_apply_redact(args.pngpath)
        pngs = os.listdir(args.pngpath)

    # pngs to text
    if args.mode == "ocr":
        directory_apply_ocr(args.pngpath, args.outfile, args.sort)

    if args.mode == "all":
        directory_apply_pdf2images(args.pdfpath, args.pngpath, args.sort)
        pngs = os.listdir(args.pngpath)
        directory_apply_ocr(args.pngpath, args.outfile, args.sort)