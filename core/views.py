from .models import Images
from .forms import imgForm
from django.shortcuts import render
from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse
from django.views import View
from django.core.cache import cache
from django.core import files
import requests
import tempfile
from PIL import Image
from io import BytesIO
import base64


class IndexView(View):
    def get(self, request):

        images = Images.objects.all()
        form = imgForm()

        context = {
            'images': images,
        }

        return render(request, 'index.html', context)

class UploadView(View):
    def get(self, request):

        form = imgForm()

        context = {
            'form': form
        }

        return render(request, 'upload.html', context)

    def post(self, request):
        imageModel = Images()
        form = imgForm(request.POST, request.FILES)
        context = {
            'form': form
        }
        if form.is_valid():
            url = form.cleaned_data['imageUrl']
            if url:
                resp = requests.get(url, stream=True)
                if resp.status_code == 200:
                    file_name = url.split('/')[-1]
                    file = tempfile.NamedTemporaryFile()
                    file.write(resp.raw.data)
                    imageModel.image.save(file_name, files.File(file))
            else:
                file = form.cleaned_data['imageFile']
                imageModel.image = file
                imageModel.save()
            return HttpResponseRedirect("/")
        else:
            render(request, 'upload.html', context=context)

class ImageView(View):
    def get(self, request, sha):
        width = request.GET.get('width', None)
        height = request.GET.get('height', None)
        image = Images.objects.get(imgHash=sha)
        c = cache.get(f"{image.pk}_{width}_{height}")
        if c:
            return HttpResponse(base64.b64decode(c), content_type="image/jpeg")
        path = f".{image.image.url}"
        if not width and not height:
            with open(path, 'rb') as f:
                return HttpResponse(f.read(), content_type="image/jpeg")
        else:
            with open(path,'rb') as f:
                data = Image.open(f).resize((int(width), int(height)))
            response = BytesIO()
            data.save(response, "JPEG")
            img_str = str(base64.b64encode(response.getvalue()))[2:-1]
            cache.set(f"{image.pk}_{width}_{height}", img_str, 120)
            return HttpResponse(response.getvalue(), content_type="image/jpeg")
