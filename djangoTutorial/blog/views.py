from django.shortcuts import render
# from django.http import HttpResponse
from .models import Post

# Create your views here.
# create function home which will handle traffic . 
# it will handle this using request variable
# This function defines what we want to do when a user go to home page


# def home(request):
#     return HttpResponse("<h1>Blog Home </h1>")

# dummy data
# posts = [
#     {
#         'author': 'CoreyMS',
#         'title': 'Blog post 1',
#         'content': 'First post content',
#         'date_posted': 'August 27,2020'
#     },
#     {
#         'author': 'CoreyMS',
#         'title': 'Blog post 1',
#         'content': 'First post content',
#         'date_posted': 'August 27,2020'
#     },

# ]

def home(request):
    context = {
        'posts' : Post.objects.all()
    }

    return render(request, 'blog/home.html',context)

# now we create we create and  we need to add the url to urls.py file in blog

def about(request):
    return render(request, 'blog/about.html',{'title': 'About title'})
