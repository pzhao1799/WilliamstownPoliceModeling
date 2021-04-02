import pytesseract as pt
import pdf2image as pdf
from PIL import Image
from deskew_utils import determine_skew

# pip3 install pytesseract, Pillow, pdf2image, scikit-image, numpy
# sudo apt-get install tesseract-ocr, poppler-utils

prepend = "./low_res"
page_file = prepend + "/test.pdf"
pages = pdf.convert_from_path(page_file, dpi = 400)

print("Finished page generation")

i = 1
for page in pages:
    image_name = prepend + "/images/page_" + str(i) + ".png"  
    page.save(image_name, "PNG")
    i+=1
    print("Finished a page...")

outfile = prepend + "/out_file.txt"  
fp = open(outfile, "w")

print("Finished pdf to image...")

for i in range(1, i):

    filename = prepend + "/images/page_" + str(i) + ".png"
    image_file = Image.open(filename)
    image_file= image_file.convert('L') # convert image to monochrome - this works
    image_file= image_file.convert('1') # convert image to black and white 
    # image_file = image_file.rotate(17)
    # angle = determine_skew(np.array(image_file)) 
    # print(angle)
    # image_file= image_file.rotate(angle)
    #osd = pt.image_to_osd(image_file)
    # print(osd)
    # angle = re.search('(?<=Rotate: )\d+', osd).group(0)
    # print("angle: ", angle)

    text = str(((pt.image_to_string(image_file, config='--psm 6'))))
    text = text.replace('-\n', '') # remove hyphens at end of lines
    fp.write(text)
    print("OCR'd a page...")

print("Finished image to text...")

fp.close()

print("OCR complete.") 
