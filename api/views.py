from django.shortcuts import render
from rest_framework import viewsets, permissions
from pdf_search.models import ChatSession, Message, PDFDocument
from .serializers import ChatSessionSerializer, MessageSerializer, PDFDocumentSerializer

# Create your views here.

class ChatSessionViewSet(viewsets.ModelViewSet):
    queryset = ChatSession.objects.all().order_by('-created')
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['id', 'title', 'created']
    search_fields = ['title']

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('created')
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['session', 'sender']
    search_fields = ['text']

class PDFDocumentViewSet(viewsets.ModelViewSet):
    queryset = PDFDocument.objects.all().order_by('-upload_date')
    serializer_class = PDFDocumentSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['session', 'title']
    search_fields = ['title', 'content']
