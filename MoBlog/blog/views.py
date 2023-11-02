from django.shortcuts import render
from . models import post


def Home(request):
    context = {
        'posts' : post.objects.all()
    }
    return render(request ,'blog/home.html' , context)


def about(request):
    return render(request , 'blog/about.html' , {'title' : 'About'})



