from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from .models import PDFDocument
from pdfminer.high_level import extract_text
# from django.conf import settings

# es = Elasticsearch(
#     [f"{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}"],
#     http_auth=(settings.ELASTICSEARCH_USERNAME, settings.ELASTICSEARCH_PASSWORD)
# )
es = Elasticsearch(['http://localhost:9200/'],
                   http_auth=('elastic', 'xvlY7Nixfrw4=9seSXnW'))

def create_index():
    index_name = 'pdf_documents'
    index_settings = {
        'settings': {
            'number_of_shards': 1,
            'number_of_replicas': 0
        },
        'mappings': {
            'properties': {
                'file': {'type': 'text'},
                'upload_date': {'type': 'date'}
            }
        }
    }

    # Create the index with settings and mappings
    es.indices.create(index=index_name, body=index_settings, ignore=400)

def index_pdf_documents():
    create_index()  # Ensure the index exists before indexing documents

    # Retrieve PDF documents from the database
    pdf_documents = PDFDocument.objects.all()
    
    # Define a generator function to prepare documents for bulk indexing
    def generate_documents():
        for pdf_document in pdf_documents:
            # Extract text from the PDF file
            text = extract_text(pdf_document.file.path)
            if text:
                yield {
                    '_index': 'pdf_documents',
                    '_id': pdf_document.id,
                    'file': text,
                    'upload_date': pdf_document.upload_date
                }
    
    # Use the Elasticsearch bulk API to index documents
    try:
        success, _ = bulk(es, generate_documents())
        print(f"Indexed {success} documents successfully.")
    except Exception as e:
        print(f"Failed to index documents: {e}")