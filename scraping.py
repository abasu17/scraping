import PyPDF2
import re
from pdf2image import convert_from_path
import os, sys
import tabula



'''	get_page_number( filename , search_header ) 
	filename : Enter full path of the PDF file.
	search_header : Enter a heading for search within PDF.
	Function will return page number. '''

def get_page_number( filename , search_header ):

	target_page = -1

	# Open PDF
	pdf_file = open(filename, "rb")

	# Read PDF
	read_pdf = PyPDF2.PdfFileReader(pdf_file)

	# Get number of Pages of given PDF
	number_of_pages = read_pdf.getNumPages()

	# Iterate all the pages to find the header
	for page_number in range(number_of_pages):
		page = read_pdf.getPage(page_number)
		page_content = page.extractText()
		page_content = re.sub(' +' , ' ' , page_content)
		if ( page_content.find(search_header.upper()) > -1 ):
			target_page = page_number
			break

	# Return target page number
	return target_page



'''	split_page( filename , page_number ) 
	filename : Enter full path of the PDF file.
	page_number : Enter page number to split PDF.
	Function will return splited file name '''
def split_page( filename , page_number ):

	# Open PDF
	pdf_file = open(filename, "rb")

	# Read PDF
	read_pdf = PyPDF2.PdfFileReader(pdf_file)

	# Initilize writer
	writer = PyPDF2.PdfFileWriter()

	# Write page
	writer.addPage(read_pdf.getPage(page_number))

	# Save in a file
	NEW_PDF_FILE_NAME = filename.split(".")[0]+"_"+str(page_number)+".pdf"
	output_file = open(NEW_PDF_FILE_NAME, "wb")
	writer.write(output_file)

	# Return filename
	return NEW_PDF_FILE_NAME



'''	pdf_to_jpg( filename ) 
	filename : Enter full path of the PDF file.
	Function will return JPEG file name '''
def pdf_to_jpg( file_name ):
	
	# Convert PDF to JPG
	pdf_to_jpg = convert_from_path(file_name , 500)
	
	# Make file name with JPG extension
	NEW_JPEG_FILE_NAME = file_name.split(".")[0] + ".jpg"
	
	# Save in a JPG file
	for img in pdf_to_jpg:
		img.save( NEW_JPEG_FILE_NAME , 'JPEG')
	
	# remove the PDF
	os.remove(file_name)

	return NEW_JPEG_FILE_NAME



'''	make_ocr( filename ) 
	filename : Enter full path of the PDF file.
	Function will return OCR file name '''
def make_ocr(file_name) :

	OUTPUT_FILE = file_name.split(".")[0]
	
	# OCR image
	os.system("tesseract " + file_name + " " + OUTPUT_FILE + " -l eng pdf")
	
	# remove the JPEG
	os.remove(file_name)
	
	return OUTPUT_FILE + ".pdf"



'''	get_table( filename ) 
	filename : Extract table from PDF file.
	Function will return table as DATA FRAME '''
def get_table(file_name):
	
	# Read PDF
	df = tabula.read_pdf(file_name)
	
	# Return Data Frame
	return df





''' EXECUTION START FROM HERE '''

if (not os.path.exists(sys.argv[1])):
	print("FileNotFoundError : File not exist\n")
	exit()

if not (sys.argv[3] != '0' or sys.argv[3] != '1'):
	print("ValueError : 3rd parameter should be boolen\n")
	exit()


FILE_NAME = sys.argv[1]
HEADER_NAME = sys.argv[2]
OCR_ENABLE = True if sys.argv[3] == str(1) else False

page_no = get_page_number( FILE_NAME , HEADER_NAME )
splited_file_name = split_page( FILE_NAME , page_no )
if OCR_ENABLE:
	new_jpeg = pdf_to_jpg(splited_file_name)
	ocr_file = make_ocr(new_jpeg)
	print(get_table(ocr_file))
else:
	print(get_table(splited_file_name))
