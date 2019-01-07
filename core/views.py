from django.shortcuts import render
from .forms import ChapterLookup


def home(request):
    search_result = {}
    print(request)
    if 'category' in request.GET:
        form = ChapterLookup(request.GET)
        if form.is_valid():
            search_result = form.search()
    else:
        form = ChapterLookup()
    return render(request, 'core/home.html', {'form': form, 'search_result': search_result})
