from django.db import models
from django.db.models.signals import post_delete


class PDFDocument(models.Model):
    file = models.FileField(upload_to='pdf_files/')
    upload_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
