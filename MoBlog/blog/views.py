from django.shortcuts import render
from . models import post
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import (  
    ListView ,
    DetailView ,
    CreateView , 
    UpdateView , 
    DeleteView
)
 
def Home(request):
    context = {
        'posts' : post.objects.all()
    }
    return render(request ,'blog/home.html' , context)


class PostListView(ListView):
    model = post
    template_name = 'blog/home.html'  # <app>/<model><viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = post

class PostCreateView(LoginRequiredMixin , CreateView):
    model = post
    fields = ['title' , 'content']

    # def form valid is the the function we need to change in order to tell the django that we need to pass in the author that we are using now
    def form_valid(self , form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin , UserPassesTestMixin,  UpdateView):
    model = post
    fields = ['title' , 'content']

    def form_valid(self , form):
        form.instance.author = self.request.user
        return super().form_valid(form) 

    # test func is because we need to see that our user passes the UserPassesTextMixin , (we use this to stop 
    # those people that are tryna edit other author`s post and we want to make sure that the
    #  pereson that is editing this post is the author of this post)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author :
            return True
        return False   


class PostDeleteView(LoginRequiredMixin , UserPassesTestMixin , DeleteView):
    model = post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author :
            return True
        return False   
    



def about(request):
    return render(request , 'blog/about.html' , {'title' : 'About'})



