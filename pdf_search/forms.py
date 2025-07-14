from django import forms

class ChatForm(forms.Form):
    user_input = forms.CharField(
        # label="Your Message",
        max_length=500,
        widget=forms.Textarea(attrs={
            "rows": 3,
            "placeholder": "Ask me anything...",
        })
    )


class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(
        label="Upload PDF Document",
        help_text="Upload a PDF file to ask questions about its content",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf',
            'id': 'pdf-upload'
        })
    )
    
    def clean_pdf_file(self):
        file = self.cleaned_data.get('pdf_file')
        if file:
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
            if file.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError("File size must be under 10MB.")
        return file


class ChatTitleForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Enter chat title...',
            'style': 'font-size: 0.9rem;'
        })
    )