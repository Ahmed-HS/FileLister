from django.shortcuts import render
from django.shortcuts import redirect

from .drive import getFiles


def login(request):
    if request.user.is_authenticated:
        return redirect("/lister/home/")
    
    return render(request,"login.html")

def home(request):
    urlToSearch = request.GET.get("url")
    urlNotFound = True if(urlToSearch is None) else False
    filesList = [] if (urlNotFound) else getFiles(request.user,urlToSearch)
    context = {"filesList" : filesList}
    pageToServe = "home.html" if(urlNotFound) else "filesList.html"
    return render(request,pageToServe,context=context)

