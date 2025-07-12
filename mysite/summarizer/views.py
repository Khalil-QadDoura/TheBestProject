from django.shortcuts import render
from .forms import UploadForm
from PyPDF2 import PdfReader
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
load_dotenv()


# 1. Load your Hugging Face token from environment
HF_TOKEN = os.getenv("HF_TOKEN", "YOUR_HUGGINGFACE_TOKEN_HERE")
client = InferenceClient(provider="hf-inference", api_key=HF_TOKEN)

def upload_view(request):
    summary = None
    form = UploadForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        # 2. Extract text from the PDF
        reader = PdfReader(request.FILES["pdf_file"])
        full_text = "\n".join(page.extract_text() or "" for page in reader.pages)

        # 3. Call the Hugging Face summarization model
        response = client.summarization(full_text, model="facebook/bart-large-cnn")
        summary = response.get("summary_text") or "Failed to generate summary."

    return render(request, "upload.html", {"form": form, "summary": summary})
