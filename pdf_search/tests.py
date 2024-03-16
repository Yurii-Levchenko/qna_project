from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import PDFDocument
from pdfminer.high_level import extract_text

class PDFTextExtractionTestCase(TestCase):
    def test_text_extraction(self):
        # Replace 'path/to/pdf_file.pdf' with the actual path to your PDF file
        pdf_path = 'C:\Projects-in-Python\pdf-qna\qna_project\pdf_files\CoffeeB_Manual_Globe_EN_10.08.2022_0UOakVl.pdf'
        pdf_path1 = 'C:\Projects-in-Python\pdf-qna\qna_project\pdf_files\stripe-2022-update.pdf'
        # Read the PDF file and extract text using pdfminer
        extracted_text = extract_text(pdf_path)
        extracted_text1 = extract_text(pdf_path1)
        
        # Write assertions to verify that the text extraction is correct
        self.assertIn('Cleaning and maintenance must not', extracted_text)
        self.assertIn(' internet economy’s long-term prospects, and we’re he', extracted_text1)

