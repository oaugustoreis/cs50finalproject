from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, logout, login
from django.urls import reverse
import requests
from .models import Category

def index(request):
    category = Category.objects.all()
    results=get_news(fromDate=None, toDate=None, topic=None, category=None, indexView=True)
    return render(request, "layout.html",{
        "results": results,
        "category": category
    })


def register_view(request):
    if request.method == "POST":
       username = request.POST['username']
       email = request.POST['email'] 
       user = User.objects.filter(username=username).first()
       if user:
           return HttpResponse("Ja existe") 
       user = User.objects.create(username=username, email=email)
       user.save()
       return HttpResponseRedirect(reverse("index")) 
    else:
       return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def login_view(request):
    if request.method == "POST":
       username = request.POST['username']
       password = request.POST['password'] 

       user = authenticate(username=username, password=password)

       if user:
          login(request, user)
          return HttpResponseRedirect(reverse("index"))
    else:
       return render(request, 'login.html')
      

def get_news(fromDate, toDate, topic,category, indexView):
    url = ""
    if indexView==True:
        url = f'https://newsapi.org/v2/everything?q=world&sortBy=popularity&language=en&apiKey=e457aaaca1c7408fa60f069dd7f27148'
    else:
        url = f'https://newsapi.org/v2/top-headlines?q={topic}&category={category}&from={fromDate}&to={toDate}&sortBy=popularity&language=en&apiKey=e457aaaca1c7408fa60f069dd7f27148'
    r = requests.get(url)
    data = r.json()
    results=[]
    articles = data['articles']
    for article in articles:
        result = {
            'title': article['title'],
            'description': article['description'],
            'url': article['url'],
            'urlimage': article['urlToImage'],
        }
        results.append(result)
    return results


def search_view(request):
    if request.method == "POST":
        inTitle = request.POST['inTitle']
        category = request.POST['category']
        fromDate=request.POST['fromDate']
        toDate=request.POST['toDate']
        results=get_news(fromDate=fromDate, toDate=toDate, topic=inTitle,category=category, indexView=False)
        return render(request, 'search.html', {
            "inTitle": inTitle,
            "fromDate": fromDate,
            "toDate": toDate,
            "result": results,
            "category": Category.objects.all()
        })
    else:
         return HttpResponseRedirect(reverse("index")) 
        