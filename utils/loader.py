from PyPDF2 import PdfReader
import os

def extract_text_from_pdf(file_path, starting_page, ending_page=None):
    pdf_reader = PdfReader(file_path)
    
    text = ""
    
    if not ending_page:
        ending_page = len(pdf_reader.pages)
    
    for page in range(starting_page, ending_page):
        text += pdf_reader.pages[page].extract_text()
    
    return text