from .models import Images
from .forms import ImageForm
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.views import View

class IndexView(View):
    def get(self, request):

        images = Images.objects.all()
        form = ImageForm()

        context = {
            'images': images,
            'form': form
        }

        return render(request, 'index.html', context)

class UploadView(View):
    @method_decorator(csrf_protect)
    def get(self, request):

        form = ImageForm()

        context = {
            'form': form
        }

        return render(request, 'upload.html', context)

    @method_decorator(csrf_protect)
    def post(self, request):

        form = ImageForm(request.POST, request.FILES)

        context = {
            'form': form
        }

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
        else:
            render(request, 'upload.html', context=context)
