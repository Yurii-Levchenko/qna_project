from django.contrib import admin
from .models import ChatSession, Message, PDFDocument, DocumentChunk

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'text', 'created')
    can_delete = True
    show_change_link = True
    ordering = ('created',)

class PDFDocumentInline(admin.TabularInline):
    model = PDFDocument
    extra = 0
    readonly_fields = ('file', 'title', 'upload_date', 'content')
    can_delete = True
    show_change_link = True
    ordering = ('-upload_date',)

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created', 'user', 'message_count', 'document_count')
    search_fields = ('id', 'title', 'user__username')
    list_filter = ('created', 'user')
    date_hierarchy = 'created'
    ordering = ('-created',)
    inlines = [MessageInline, PDFDocumentInline]
    readonly_fields = ('id', 'created')

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'

    def document_count(self, obj):
        return obj.documents.count()
    document_count.short_description = 'Documents'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'sender', 'short_text', 'created')
    search_fields = ('text', 'session__title', 'sender')
    list_filter = ('sender', 'created')
    date_hierarchy = 'created'
    ordering = ('-created',)
    readonly_fields = ('created',)

    def short_text(self, obj):
        return (obj.text[:50] + '...') if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Text'

@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'session', 'user', 'upload_date', 'file_link')
    search_fields = ('title', 'content', 'session__title', 'user__username')
    list_filter = ('upload_date', 'session', 'user')
    date_hierarchy = 'upload_date'
    ordering = ('-upload_date',)
    readonly_fields = ('upload_date', 'content')

    def file_link(self, obj):
        if obj.file:
            return f'<a href="{obj.file.url}" target="_blank">Download</a>'
        return "-"
    file_link.allow_tags = True
    file_link.short_description = 'File'

@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'chunk_index', 'short_content')
    search_fields = ('document__title', 'content')
    list_filter = ('document',)
    ordering = ('document', 'chunk_index')
    readonly_fields = ('chunk_index',)

    def short_content(self, obj):
        return (obj.content[:50] + '...') if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'