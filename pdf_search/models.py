from django.db import models
import logging
from django.db.models.signals import post_delete
from django.dispatch import receiver
from elasticsearch import Elasticsearch

# logger = logging.getLogger(__name__)


class PDFDocument(models.Model):
    file = models.FileField(upload_to='pdf_files/')
    upload_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)



# """Whenever a PDFDocument instance is deleted, 
#     it will trigger this function, which in turn 
#     deletes the corresponding document from 
#     the Elasticsearch index 'pdf_index'."""
# @receiver(post_delete, sender=PDFDocument)
# def delete_document_from_elasticsearch(sender, instance, **kwargs):
#     es = Elasticsearch(['http://localhost:9200/'], http_auth=('elastic', 'xvlY7Nixfrw4=9seSXnW'))
#     try:
#         es.delete(index='pdf_index', id=str(instance.id))
#     except Exception as e:
#         # Log the error
#         logger.error(f"Error occurred while deleting document {instance.id} from Elasticsearch index: {e}")