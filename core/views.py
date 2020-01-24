from django.shortcuts import render
from .forms import UploadImageForm

def main_page(request):
    return render(request, 'index.html')

def upload_page(request):
    form = UploadImageForm()
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return render(request, 'upload.html', {'form': form})