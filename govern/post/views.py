from django.shortcuts import render
from .models import Post
# Create your views here.

def home(request):
    # return HttpResponse("<h1> Site home </h1>")
    context = {
        "posts": Post.objects.all(),
        "title": "POSTS"}
    return render(request, 'post/home.html', context)


def about(request):
    # return HttpResponse("<h1> ABOUT </h1>")
    return render(request, 'post/about.html')
