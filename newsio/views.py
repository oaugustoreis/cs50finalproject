from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, logout, login
from django.urls import reverse
import requests, json
from .models import Category, Saved

def index(request):
    category = Category.objects.all()
    savedUrl = Saved.objects.all()
    results=get_news(fromDate=None, toDate=None, topic=None, category=None, indexView=True)
    paginator = Paginator(results, 10)
    results = paginator.get_page(request.GET.get('page'))
    return render(request, "layout.html",{
        "savedUrl": savedUrl,
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
        if article['urlToImage']:
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
        

from django.http import JsonResponse
def saved_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data['url']
        title = data['title']
        description = data['description']
        image_url = data['image_url']

        # Save the data to your database
        url_saved = Saved.objects.filter(url=url).first()
        if not url_saved:
            saved_url = Saved(title=title, url=url, description=description, image_url=image_url)
            saved_url.save()
        return JsonResponse({'message': 'URL saved successfully'}) 
def delete_saved(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data['url']
        Saved.objects.filter(url=url).delete()
        return JsonResponse({'message': 'URL deleted successfully'})




def read_later(request):
    savedUrl = Saved.objects.all()
    return render(request, 'saved.html', {
        "savedUrl": savedUrl
    })
