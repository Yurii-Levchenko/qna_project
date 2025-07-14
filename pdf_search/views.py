from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .forms import ChatForm, PDFUploadForm, ChatTitleForm
from .models import ChatSession, Message, PDFDocument
from .utils import generate_response, extract_text_from_pdf

def home(request):
    return render(request, 'pdf_search/home.html')


def new_chat(request):
    session = ChatSession.objects.create()
    return redirect('pdf_search:chat', id=str(session.id))


def chat_view(request, id):
    session = get_object_or_404(ChatSession, id=id)
    chat_form = ChatForm()
    upload_form = PDFUploadForm()

    # fetch all chat sessions for sidebar (optionally filtering by user will be added soon)
    all_sessions = ChatSession.objects.order_by('-created')

    if request.method == 'POST':
        # handle PDF upload
        if 'pdf_file' in request.FILES:
            upload_form = PDFUploadForm(request.POST, request.FILES)
            if upload_form.is_valid():
                pdf_file = upload_form.cleaned_data['pdf_file']
                
                # create PDF document
                pdf_document = PDFDocument.objects.create(
                    file=pdf_file,
                    session=session,
                    title=pdf_file.name
                )
                
                # extracting text from PDF
                try:
                    text_content = extract_text_from_pdf(pdf_file)
                    pdf_document.content = text_content
                    pdf_document.save()
                    
                    messages.success(request, f"PDF '{pdf_file.name}' uploaded successfully! You can now ask questions about it.")
                except Exception as e:
                    messages.error(request, f"Error processing PDF: {str(e)}")
                    pdf_document.delete()
                
                return redirect('pdf_search:chat', id=session.id)
        
        # handle chat message
        elif 'user_input' in request.POST:
            chat_form = ChatForm(request.POST)
            if chat_form.is_valid():
                user_input = chat_form.cleaned_data['user_input']

                recent_messages = session.messages.order_by('-created')[:3][::-1]
                ai_response = generate_response(user_input, recent_messages, session)

                Message.objects.create(session=session, sender='user', text=user_input)
                Message.objects.create(session=session, sender='ai', text=ai_response)

                # auto-generate title from first user message if not set
                if not session.title:
                    session.save()  # triggers auto-title generation in the model

                return redirect('pdf_search:chat', id=session.id)

    chat_history = session.messages.order_by('created')
    uploaded_documents = session.documents.all()

    return render(request, 'pdf_search/chat.html', {
        'chat_form': chat_form,
        'upload_form': upload_form,
        'chat_history': chat_history,
        'session': session,
        'uploaded_documents': uploaded_documents,
        'all_sessions': all_sessions,
    })


def delete_document(request, session_id, document_id):
    """Delete a PDF document from the chat session"""
    if request.method == 'POST':
        session = get_object_or_404(ChatSession, id=session_id)
        document = get_object_or_404(PDFDocument, id=document_id, session=session)
        document.delete()
        messages.success(request, f"Document '{document.title}' deleted successfully.")
        return redirect('pdf_search:chat', id=session_id)
    
    return redirect('pdf_search:chat', id=session_id)


def delete_chat(request, session_id):
    """Delete a chat session and all its associated data"""
    if request.method == 'POST':
        session = get_object_or_404(ChatSession, id=session_id)
        
        # store session info for success message
        session_info = f"Chat from {session.created.strftime('%M d, %H:%M')}"
        
        # delete the session (this will cascade delete messages and documents)
        session.delete()
        
        messages.success(request, f"{session_info} deleted successfully.")
        
        # redirect to home or the most recent chat
        latest_session = ChatSession.objects.order_by('-created').first()
        if latest_session:
            return redirect('pdf_search:chat', id=latest_session.id)
        else:
            return redirect('pdf_search:home')
    
    # if not POST, redirect to the chat
    return redirect('pdf_search:chat', id=session_id)


def edit_chat_title(request, session_id):
    """Edit chat title via AJAX or form submission"""
    session = get_object_or_404(ChatSession, id=session_id)
    
    if request.method == 'POST':
        form = ChatTitleForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data['title'].strip()
            if new_title:
                session.title = new_title
                session.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    # AJAX request
                    return JsonResponse({
                        'success': True,
                        'title': session.title,
                        'message': 'Chat title updated successfully.'
                    })
                else:
                    # regular form submission
                    messages.success(request, 'Chat title updated successfully.')
                    return redirect('pdf_search:chat', id=session.id)
            else:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Title cannot be empty.'
                    }, status=400)
                else:
                    messages.error(request, 'Title cannot be empty.')
                    return redirect('pdf_search:chat', id=session.id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid title format.'
                }, status=400)
            else:
                messages.error(request, 'Invalid title format.')
                return redirect('pdf_search:chat', id=session.id)
    
    # GET request - show form
    form = ChatTitleForm(initial={'title': session.title})
    return render(request, 'pdf_search/edit_chat_title.html', {
        'form': form,
        'session': session
    })
