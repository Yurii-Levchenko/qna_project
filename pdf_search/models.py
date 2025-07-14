from django.db import models
from django.contrib.auth.models import User
import uuid


class PDFDocument(models.Model):
    file = models.FileField(upload_to='pdf_files/')
    title = models.CharField(max_length=255, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session = models.ForeignKey('ChatSession', on_delete=models.CASCADE, null=True, blank=True, related_name='documents')
    
    def __str__(self):
        return self.title or self.file.name
    
    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.file.name
        super().save(*args, **kwargs)


class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def messages(self):
        return self.messages.all()

    def __str__(self):
        return self.title or f"Chat {self.created.strftime('%M d, %H:%M')}"
    
    def save(self, *args, **kwargs):
        # auto-generate title from first user message if not set
        if not self.title and self.pk:
            first_user_message = self.messages.filter(sender='user').first()
            if first_user_message:
                # truncate to 50 characters and clean up
                title = first_user_message.text.strip()[:50]
                if len(first_user_message.text) > 50:
                    title += "..."
                self.title = title
        super().save(*args, **kwargs)


class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('ai', 'AI')])
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        preview = (self.text[:30] + '...') if len(self.text) > 30 else self.text
        return f"{self.sender.capitalize()} @ {self.created.strftime('%Y-%m-%d %H:%M:%S')}:{preview}"


class DocumentChunk(models.Model):
    """model to store chunked content from PDFs for RAG"""
    document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, related_name='chunks')
    content = models.TextField()
    chunk_index = models.IntegerField()
    embedding = models.JSONField(null=True, blank=True)  # stores embeddings as JSON
    
    class Meta:
        ordering = ['chunk_index']
    
    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.document.title}"