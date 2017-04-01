from django.shortcuts import render
import models
from django.http import HttpResponse
# Create your views here.


def home(request):
    articles = models.Article.objects.all()
    return render(request, 'index.html', {'articles': articles})


