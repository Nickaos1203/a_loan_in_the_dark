from django.shortcuts import render
from news.models import New
from django.views import View
from news.forms import NewsForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect

import datetime

# Create your views here.
def get_all_news(request):
    news_list = New.objects.all()
    return render(request,"news/news_listing.html", context={"news_list": news_list})


def news_detail(request, id):
    news = New.objects.get(id=id)
    return render(request,"news/news_detail.html", context={"news": news})


def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            current_news = form.save(commit=False)
            current_news.author = request.user
            current_news.save()

            return redirect('news:all_news')
    else:
        form = NewsForm()
    return render(request, "news/create_news_form.html", {"form": form})

    