****PDF Q&A Application****
LLM Searching in Python, Djano using Elasticsearch

This is a Python Django web application designed to allow users to upload PDF documents and ask questions related to the content of those documents. The application uses Elasticsearch for indexing and searching through the uploaded documents.

**Installation**
1. Clone the repository to your local machine:
  git clone https://github.com/Yurii-Levchenko/qna_project.git

2. Navigate to the project directory:
   cd qna_project

3. Activate the existing virtual environment:
   On Windows:
     venv\Scripts\activate
   On macOS and Linux:
     source venv/bin/activate

4. Install the required dependencies:
   pip install -r requirements.txt

**Usage**
Note: Before using the application provide your own Elasticsearch login data in settings.py of this project.
      Replace author's ELASTICSEARCH_USERNAME and ELASTICSEARCH_PASSWORD with your own.

1. Run the Django development server:
2. Access the application in your web browser at http://localhost:8000.
3. Navigate to the "Upload PDF" page to upload PDF documents.
  Click on the "Choose File" button to select a PDF file from your local machine.
  Click on the "Upload" button to upload the selected PDF file.
  Repeat the above steps to upload additional PDF documents.

4. Once the PDF documents are uploaded, navigate to the "Ask Me" page to ask questions related to the content of the uploaded documents.
  Type your question in the input field provided.
  Click on the "Ask" button to submit your question.
  The application will search through the uploaded documents and provide relevant answers based on the content.

Note: Searching works partially for now, the project will be updated and provided with enhenced querying and searching.