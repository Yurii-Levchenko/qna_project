from django.urls import path
from .views import home, chat_view, new_chat, delete_document, delete_chat, edit_chat_title


app_name = "pdf_search"

urlpatterns = [
    path('', home, name='home'),
    path('new/', new_chat, name='new_chat'),
    path('chat/<str:id>/', chat_view, name='chat'),
    path('chat/<str:session_id>/delete-document/<int:document_id>/', delete_document, name='delete_document'),
    path('chat/<str:session_id>/delete/', delete_chat, name='delete_chat'),
    path('chat/<str:session_id>/edit-title/', edit_chat_title, name='edit_chat_title'),
]