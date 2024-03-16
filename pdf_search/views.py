from django.shortcuts import render, redirect
from .models import PDFDocument
from pdfminer.high_level import extract_text

from django.conf import settings

from .elasticsearch_operations import index_pdf_documents




def search_question(request):
    # Your logic for the question and response page goes here
    return render(request, 'pdf_search/qna.html')

def upload_pdf(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        pdf_document = PDFDocument.objects.create(file=pdf_file)
        # Extract text from the uploaded PDF file
        text = extract_text(pdf_document.file.path)
        # Store extracted text in Elasticsearch or Apache Solr
        # (implementation details depend on the chosen search engine)
        # Alternatively, you can process the text further or store it in the database

        index_pdf_documents()

        return redirect('upload_pdf')
    return render(request, 'pdf_search/upload_pdf.html')

# def pdf_detail(request, pk):
#     pdf_document = PDFDocument.objects.get(pk=pk)
#     return render(request, 'pdf_detail.html', {'pdf_document': pdf_document})
