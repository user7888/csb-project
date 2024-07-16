from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from .models import BlogPost
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
import sqlite3

# For broken authentication flaw
User = get_user_model()
def get_user_from_session(session_key):
    try:
        session = Session.objects.get(session_key=session_key)
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        return User.objects.get(id=user_id)
    except (Session.DoesNotExist, User.DoesNotExist):
        return None

def indexView (request):
    session_id = request.GET.get('sessionid')              # Remove from Broken Authentication from fix
    context = {'sessionid':session_id}                     # Remove from Broken Authentication from fix
    return render(request, 'blogs/index.html', context)    # Remove from Broken Authentication from fix
    #return render(request, 'blogs/index.html')            # Broken authentication fix

def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                session_id = request.session.session_key
                redirect_url = f'/blogs/?sessionid={session_id}'
                return redirect(redirect_url)              # Remove from Broken Authentication from fix
                #return redirect('blogs:index')            # Broken Authentication fix
        else:
            return redirect('blogs:index')
    else:
        return redirect('blogs:index')
        

def logoutView(request):
    if request.method == 'POST':
        logout(request)
        return redirect('blogs:index')
    return HttpResponse(status=405)

#@login_required                                                        # Broken authentication fix
def addBlogPostView(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            query = f"INSERT INTO blogs_blogpost (title, text_content, author_id, pub_date) VALUES ('{title}', '{content}', {request.user.id}, '{timezone.now()}')"

            cursor.executescript(query)
            connection.commit()
            connection.close()
            #BlogPost.objects.create(                                   # SQL injection fix
            #    title=title,                                           # SQL injection fix
            #    text_content=content,                                  # SQL injection fix
            #    author=request.user,                                   # SQL injection fix
            #    pub_date=timezone.now())                               # SQL injection fix
            session_id = request.GET.get('sessionid')                   # Remove from broken authentication fix
            redirect_url = f'/blogs/blog_posts/?sessionid={session_id}' # Remove from broken authentication fix
            return redirect(redirect_url)                               # Remove from broken authentication fix
            #return redirect('blogs:blog_posts')                        # Broken authentication fix
        
    return render(request, 'blogs:index')

#@login_required                                                       # Broken authentication fix
def BlogPostsView(request):
    session_id = request.GET.get('sessionid')                         # Remove from Broken Authentication fix
    user = get_user_from_session(session_id) if session_id else None  # Remove from Broken Authentication fix
    if user is None:                                                  # Remove from Broken Authentication fix
        return HttpResponse("Invalid session ID or session expired")  # Remove from Broken Authentication fix

    blog_posts = BlogPost.objects.all().order_by('-pub_date')
    return render(request, 
                  'blogs/blog_posts.html', 
                  {'blog_posts': blog_posts, 
                   'current_user':request.user,
                   'sessionid': session_id})                           # Remove from Broken Authentication fix

def detailView(request, blog_post_id):
    blog_post = get_object_or_404(BlogPost, pk=blog_post_id)

    return render(request, 'blogs/detail.html', {
        'blog_post': {
            'title':blog_post.title,
            'text_content': mark_safe(blog_post.text_content)   # Remove from XSS fix
            # 'text_content': (blog_post.text_content)          # XSS fix
        }
    })

def resultsView(request, blog_post_id):
    blog_post = get_object_or_404(BlogPost, pk=blog_post_id)
    return render(request, 'blogs/results.html', {'BlogPost': blog_post})

#@login_required                                                        # Broken authentication fix
def deleteView(request, blog_post_id):
    session_id = request.GET.get('sessionid')                           # Remove from broken authentication fix
    user = get_user_from_session(session_id) if session_id else None    # Remove from broken authentication fix
    if user is None:                                                    # Remove from broken authentication fix
        return HttpResponse("Invalid session ID or session expired")    # Remove from broken authentication fix

    if request.method == 'GET':                                         # Remove from CSRF fix
    #if request.method == 'POST':                                       # CSRF fix
        blog_post = get_object_or_404(BlogPost, pk=blog_post_id)

        blog_post.delete()                                              # Remove from broken access control fix
        redirect_url = f'/blogs/blog_posts/?sessionid={session_id}'     # Remove from broken authentication fix
        return redirect(redirect_url)                                   # Remove from broken authentication fix   
        #return redirect('blogs:blog_posts')                            # Broken authenticaton fix

    # For Broken Access Control vulnerability fix (lines 123-127)
        #if blog_post.author == request.user:                           # Broken access control fix
        #    blog_post.delete()                                         # Broken access control fix
        #    return redirect('blogs:blog_posts')                        # Broken access control fix
        #else:                                                          # Broken access control fix
        #    return HttpResponse("Not authorized")                      # Broken access control fix
    else:
        #return HttpResponseNotAllowed(['POST'])                        # Broken access control fix
        return HttpResponse(status=405)                                 # Remove from broken access control fix