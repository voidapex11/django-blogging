from django.http import HttpResponse
from django.template import loader

def home(request):
  template = loader.get_template('home/index.html')
  return HttpResponse(template.render())

def disclaimer(request):
  template = loader.get_template('home/disclaimer.html')
  return HttpResponse(template.render())