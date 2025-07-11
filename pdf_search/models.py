from django.db import models
import uuid


class PDFDocument(models.Model):
    file = models.FileField(upload_to='pdf_files/')
    upload_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)


class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def messages(self):
        return self.messages.all()

    def __str__(self):
        return str(self.id)


class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('ai', 'AI')])
    text =models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        preview = (self.text[:30] + '...') if len(self.text) > 30 else self.text
        return f"{self.sender.capitalize()} @ {self.created.strftime('%Y-%m-%d %H:%M:%S')}:{preview}"