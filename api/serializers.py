from rest_framework import serializers
from pdf_search.models import ChatSession, Message, PDFDocument

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'session', 'sender', 'text', 'created']

class PDFDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFDocument
        fields = ['id', 'file', 'title', 'upload_date', 'content', 'session']

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    documents = PDFDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ['id', 'title', 'created', 'messages', 'documents'] 