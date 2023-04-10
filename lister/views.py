from django.shortcuts import render
from django.shortcuts import redirect

from .drive import getFiles


def login(request):
    if request.user.is_authenticated:
        return redirect("/lister/home/")

    return render(request, "login.html")


def home(request):
    if not request.user.is_authenticated:
        return redirect("/lister/login/")

    folderId = request.GET.get("folderId","root")
    filesList = getFiles(request.user, folderId)
    context = {"filesList": filesList , "folderId" : folderId}
    return render(request, "home.html", context=context)
