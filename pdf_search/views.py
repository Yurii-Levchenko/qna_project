from django.shortcuts import render, redirect
from .models import PDFDocument
from pdfminer.high_level import extract_text

from django.conf import settings

from .elasticsearch_operations import index_pdf_documents
from elasticsearch import Elasticsearch
from django.http import JsonResponse
from elasticsearch_dsl import Search, Q

es = Elasticsearch(['http://localhost:9200/'])

# def search_question(request):
#     if request.method == 'POST':
#         user_question = request.POST.get('user_question', '')




def search_question(request):
    if request.method == 'POST':
        user_question = request.POST.get('user_question', '')
        print('User question:', user_question)
        # Build a more complex Elasticsearch query using Query DSL
        # query = {
        #     "query": {
        #         "bool": {
        #             "should": [
        #                 {"match": {"file": {"query": user_question, "boost": 3}}},
        #                 {"match_phrase": {"file": {"query": user_question, "slop": 50, "boost": 2}}},
        #                 # Add more query types as needed
        #             ]
        #         }
        #     }
        # }

        # returns a file which contains provided word
        query = {
            "query": {
                "match": {
                    "content": {
                        "query": user_question,
                        "minimum_should_match": "40%"
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

        try:
            # Perform the search using Elasticsearch DSL
            response = es.search(index='pdf_documents', body=query)

            # Extract relevant information from search results
            # if response['hits']['total']['value'] > 0:
            #     # Extract relevant content from the matched documents
            #     relevant_content = [hit['_source']['file'] for hit in response['hits']['hits']]
            #     # You may need to further process the content to extract structured answers
                
            #     # For now, let's concatenate the content into a single string
            #     answer = '\n'.join(relevant_content)
            
            # Extract relevant information from search results
            if response['hits']['total']['value'] > 0:
                relevant_chunks = []
                for hit in response['hits']['hits']:
                    # Extract relevant content chunk
                    chunk = hit['highlight']['content'][0]
                    relevant_chunks.append(chunk)

                # Concatenate relevant chunks into a single string
                answer = '\n'.join(relevant_chunks)
            else:
                answer = "Sorry, I couldn't find an answer to your question."

            # Return the answer as JSON response
            return JsonResponse({'answer': answer})
        except Exception as e:
            # Return an error message if any exception occurs during the search
            return JsonResponse({'error': str(e)}, status=500)

    # If the request method is not POST or if there's no question, return an empty response
    return render(request, 'pdf_search/qna.html')

def upload_pdf(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        pdf_document = PDFDocument.objects.create(file=pdf_file)
        # Extract text from the uploaded PDF file
        text_content = extract_text(pdf_document.file.path)

        # Store the extracted text content in the content field
        pdf_document.content = text_content
        pdf_document.save()

        index_pdf_documents()

        return redirect('upload_pdf')
    return render(request, 'pdf_search/upload_pdf.html')

"""
def pdf_detail(request, pk):
    pdf_document = PDFDocument.objects.get(pk=pk)
    return render(request, 'pdf_detail.html', {'pdf_document': pdf_document})
"""

# ver1
"""
def search_question(request):
    if request.method == 'POST':
        # Get the user's question from the request
        user_question = request.POST.get('user_question', '')
        # csrf_token = request.headers.get('X-CSRFToken', '')
        print("User's question:", user_question)
        # print("CSRF Token:", csrf_token) #just to make sure it's being parsed properly

        if not user_question:
            return JsonResponse({'error': 'Empty question'}, status=400)

        # Query Elasticsearch using a more advanced search query
        es_query = {
            "query": {
                "match": {
                    "file": {
                        "query": user_question,
                        "operator": "and"
                    }
                }
            }
        }
        print("Elasticsearch Query:", es_query)

        try:
            # Perform Elasticsearch search
            search_results = es.search(index='pdf_documents', body=es_query)

            # Extract the answer from the search results (you may need to customize this based on your data structure)
            if search_results['hits']['total']['value'] > 0:
                # Assuming you're extracting the first hit as the answer
                answer = search_results['hits']['hits'][0]['_source']['file']
            else:
                answer = "Sorry, I couldn't find an answer to your question."

            # Return the answer as JSON response
            return JsonResponse({'answer': answer})
        except Exception as e:
            # Return an error message if any exception occurs during the search
            return JsonResponse({'error': str(e)}, status=500)

    # If the request method is not POST or if there's no question, return an empty response
    return render(request, 'pdf_search/qna.html')
    """
