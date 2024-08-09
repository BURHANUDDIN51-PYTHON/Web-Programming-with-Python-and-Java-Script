from markdown2 import Markdown
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import random
from django import forms  
from . import util




def markdown_to_html(content):
    markdowner = Markdown()
    return markdowner.convert(content)
    
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })
    
def title(request, title):
    content = util.get_entry(title)
    if not content:
        return render(request, "encyclopedia/error.html")
    converted_content = markdown_to_html(content)
    return render(request, "encyclopedia/title.html", {
        "content":converted_content,
        "title":title
        })

def search(request):
    if request.method == "POST":
        query = request.POST.get("q")
        entries = util.list_entries()
        matched_query =[]
        for entry in entries:
            if query.lower() == entry.lower():
                return HttpResponseRedirect(f"wiki/{entry}")
            if query.lower() in entry.lower():
                matched_query.append(entry)
        return render(request, 'encyclopedia/result.html', {
            "entries":matched_query,
        })  
          
        
def new_page(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('markdown')
        entries = util.list_entries()
        if not title or not content:
            return render(request, 'encyclopedia/error.html',{'message':'Fill the missing fields'})
        if title in entries:
            return render(request, 'encyclopedia/error.html',{'message':"The title already Exists"})
        util.save_entry(title, content)
        return HttpResponseRedirect(f'wiki/{title}')
    else:
        return render(request, 'encyclopedia/new.html')


def edit_page(request):
    if request.method == "POST":
        content = util.get_entry(request.POST.get('title'))
        return render(request, 'encyclopedia/edit.html', {
            'content':content,
            'title': request.POST.get('title')
        })
        
def save_changes(request):
    if request.method == "POST":
        util.save_entry(request.POST.get('title'), request.POST.get('content'))
        return HttpResponseRedirect(f'wiki/{request.POST.get("title")}')
    
def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return HttpResponseRedirect(f'wiki/{random_entry}')
    
        
        
        
           
       
       


