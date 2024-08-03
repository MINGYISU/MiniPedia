from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404

from random import choice
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), 
        "rand": choice(util.list_entries())
    })

def get(request, name=None):
    if name is None:
        raise Http404("The name of the file to search is not provided!")
    file = util.get_entry(name)
    if file is None:
        raise Http404("Page Not Found! Try using another entry!")
    return render(request, "encyclopedia/entrypage.html", {
        "name": name, 
        "entry": markdown(file), 
        "rand": choice(util.list_entries())
    })

def search(request):
    if request.method == "POST":

        # extract the name of the user inputted value
        name = request.POST["q"]
        file = util.get_entry(name)

        # if a file is found
        if file is not None:
            # go to the page of that file
            url = reverse('get', args=[name])
            return redirect(url)
        
        lst = []
        files = util.list_entries()
        for ele in files:
            if name.upper() in ele.upper():
                lst.append(ele)
        # return a list of the matched filenames
        return render(request, "encyclopedia/search.html", {
            "toSearch": name, 
            "entries": sorted(lst), 
            "rand": choice(util.list_entries())
        })
    else:
        # Doesn't allow user to reach this url, ie, request method is get
        raise Http404("Page Not Found")

def create(request):
    if request.method == "POST":
        name = request.POST["name"]
        content = request.POST["content"]
        if util.get_entry(name) is not None:
            raise Http404("Save Failed! Reason: " + name + " Already exists!")
        util.save_entry(name, content)
        url = reverse('get', args=[name])
        return redirect(url)
    else:
        # if getting, return the create page
        return render(request, "encyclopedia/newpage.html", {
            "rand": choice(util.list_entries())
        })

def edit(request, name=None):
    if request.method == "POST":
        newContent = request.POST["content"]
        if util.get_entry(name) != newContent:
            util.save_entry(name, newContent)
        url = reverse('get', args=[name])
        return redirect(url)
    elif request.method == "GET":
        if util.get_entry(name) is None:
            raise Http404("Page Not Found!")
        return render(request, "encyclopedia/editpage.html", {
            "name": name, 
            "entry": util.get_entry(name), 
            "rand": choice(util.list_entries())
        })
