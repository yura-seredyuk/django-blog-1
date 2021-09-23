from django import forms
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from blog import *
from .models import Post
from .forms import PostForm, ContactForm, LoginForm, CommentForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required
# Create your views here.

# GET METHOD
def post_list(request):
    posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date')
    return render(request, 'blog/post_lists.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post':post,'comments': comments,'comment_form': comment_form})

# POST METHOD
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})


# UPDATE METHOD
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form, 'pk':pk})

# DELETE METHOD
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post:
        post.delete()
        posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date')
        return render(request, 'blog/post_lists.html', {'posts':posts})


# MAIL
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Test message"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())
            try:
                send_mail(subject, message, 
                          'yurii.seredyuk@gmail.com',
                          ['yurii.seredyuk@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Find incorrect header')
            return redirect("success")

    form = ContactForm()
    return render(request, "blog/contact.html", {'form': form})

def success_view(request):
    return HttpResponse('Accepted! Thank you for your message.')

# LOGIN
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})
