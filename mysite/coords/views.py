# Create your views here.

from django.shortcuts import HttpResponse

def index(request):
    return HttpResponse("Hello, world.")
    template = loader.get_template('coords/index.html')
    return HttpResponse(template.render(context))