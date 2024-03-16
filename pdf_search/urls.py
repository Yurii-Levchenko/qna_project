from django.urls import path
from .views import upload_pdf, search_question

urlpatterns = [
    path('upload/', upload_pdf, name='upload_pdf'),
    path('', search_question, name='qna_page'),
]