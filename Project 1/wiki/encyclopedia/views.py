from django.shortcuts import render
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
import random


class SearchForm(forms.Form):
    search = forms.CharField(label="Search Encyclopedia")

class PageForm(forms.Form):
    title = forms.CharField(label="Title", required=True)
    content = forms.CharField(label="Content", widget=forms.Textarea, required=True)

def index(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        title = form.cleaned_data["search"]
        return HttpResponseRedirect(f"wiki/{title}")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm()
    })


def wiki(request, title):
    exists = util.get_entry(title)
    if exists is None:
        pages = util.list_entries()
        search_results = []
        for page in pages:
            if title.lower() in page.lower():
                search_results.append(page)
        return render(request, "encyclopedia/search.html", {
            "title": title,
            "entries": search_results,
            "search_form": SearchForm()
        })

    return render(request, "encyclopedia/wiki.html", {
        "title": title,
        "markdown": markdown2.markdown(util.get_entry(title)),
        "search_form": SearchForm()
    })


def new_page(request):
    form = PageForm(request.GET)
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]

        page_exists = util.get_entry(title)
        if page_exists is None:
            util.save_entry(title, content)
            return HttpResponseRedirect(f"wiki/{title}")
        else:
            return render(request, "encyclopedia/newpage.html", {
                "error": True,
                "page_form": PageForm(),
                "search_form": SearchForm()
            })
    else:
        return render(request, "encyclopedia/newpage.html", {
            "page_form": PageForm(),
            "search_form": SearchForm()
        })

def edit_page(request, title):
    content = util.get_entry(title)
    form_data = {
        "title": title,
        "content": content
    }
    form = PageForm(form_data)

    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")

    return render(request, "encyclopedia/editpage.html", {
        "title": title,
        "search_form": SearchForm(),
        "page_form": form
    })


def random_page(request):
    pages = util.list_entries()
    random_page = random.choice(pages)
    return HttpResponseRedirect(f"wiki/{random_page}")
