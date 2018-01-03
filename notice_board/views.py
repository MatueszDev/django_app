# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def add_post(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save()
            new_post.save()
    else:
        post_form = PostForm()
    return render(request, 'post/list.html', {'posts': posts, 'post_form': post_form})


@login_required
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, publish__year=year,
                             publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.name = User.objects.get(username=request.user)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'post/detail.html', {'post': post, 'comments': comments,
                                                'comment_form': comment_form})

