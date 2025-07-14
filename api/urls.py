from rest_framework.routers import DefaultRouter
from .views import ChatSessionViewSet, MessageViewSet, PDFDocumentViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'chats', ChatSessionViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'documents', PDFDocumentViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 