from django.shortcuts import render, redirect
from .models import PDFDocument
from .utils import extract_text_from_pdf
from .elasticsearch_operations import index_pdf_documents
from elasticsearch import Elasticsearch
from django.http import JsonResponse
import re

es = Elasticsearch(['http://localhost:9200/'])

def search_question(request):
    if request.method == 'POST':
        user_question = request.POST.get('user_question', '')

        # making sure that user's question reaches backend
        print('User question:', user_question)

        # this query works partially
        query = {
            "query": {
                "multi_match": {
                    "query": user_question,
                    "fields": ["content"]
                }
            },
            "highlight": {
                "fields": {
                    "content": {}
                }
            },
            "sort": [
                {"_score": {"order": "desc"}}
            ]
        }

        try:
            # search with elasticsearch DSL
            response = es.search(index='pdf_documents', body=query)
            
            # relevant information extraction (from search results)
            if response['hits']['total']['value'] > 0:
                relevant_paragraphs = []
                for hit in response['hits']['hits']:
                    # extraction of relevant content chunk
                    highlighted_content = hit['highlight']['content'][0]
                    
                    # splitting the content into chunks
                    paragraphs = re.split(r'\n\s*\n', highlighted_content)

                    # filtering out empty strings and adding to relevant_chunks
                    relevant_paragraphs.extend(filter(None, paragraphs))
                    
                answer = '\n\n'.join(relevant_paragraphs)
            else:
                answer = "Sorry, I couldn't find an answer to your question."

            return JsonResponse({'answer': answer})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'pdf_search/qna.html')

def upload_pdf(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        pdf_document = PDFDocument.objects.create(file=pdf_file)

        text_content = extract_text_from_pdf(pdf_document.file.path)
        pdf_document.content = text_content

        pdf_document.save()

        # refers to elasticsearch_operations.py
        index_pdf_documents()

        return redirect('upload_pdf')
    return render(request, 'pdf_search/upload_pdf.html')

"""
one of queries tried
        query = {
                    "query": {
                        "match": {
                            "content": {
                                "query": user_question,
                                "minimum_should_match": "70%"
                                # "operator": "and"
                            }
                        }
                    },
                    "highlight": {
                        "fields": {
                            "content": {}
                        }
                    },
                    "sort": [
                        {"_score": {"order": "desc"}}
                    ]
                }
        """