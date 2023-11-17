from django.shortcuts import render , get_object_or_404
from . models import post
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.auth.models import User
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
    paginate_by = 6   #this is where we say how many posts we want to show on every page

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
    

class UserPostListView(ListView):
    model = post
    template_name = 'blog/user_posts.html'  # <app>/<model><viewtype>.html
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User , username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')


def about(request):
    return render(request , 'blog/about.html' , {'title' : 'About'})



