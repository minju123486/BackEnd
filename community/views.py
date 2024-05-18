from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
import openai
import os
import environ

from rest_framework.permissions import IsAuthenticated
user_data = dict()

from pathlib import Path
from django.shortcuts import render 
from django.http import JsonResponse
from myapp import gpt_prompt
import openai
import os
from myapp.models import course, professor_lecture, student_lecture, problem, answer
from Login.models import school
from datetime import datetime
from .models import post, comment, like_check

@api_view(['POST'])   
def post_create(request): # for professor
    post_title = request.data.get('title')
    post_author = 'hahahahaaha'
    post_content = request.data.get('content')
    print(post_title, post_author,post_content)
    now = datetime.now()


    n_year = now.year
    n_month = now.month
    n_day = now.day
    n_hour = now.hour
    n_minute = now.minute
    tempt = post(title = post_title, content = post_content, author = post_author, year = n_year, month = n_month, day = n_day, hour = n_hour, minute = n_minute, watch = 0, like = 0, comment_number = 0)
    tempt.save()
    return Response({'message':'success'}, status = 200)



@api_view(['POST'])   
def post_like(request): # for professor
    post_id = request.data.get('id')
    post = post.objects.get(id=post_id)
    post.like += 1
    post.save()
    return Response({'message':'success'}, status = 200)


@api_view(['POST'])   
def post_dislike(request): # for professor
    post_id = request.data.get('id')
    post = post.objects.get(id=post_id)
    post.like -= 1
    post.save()
    return Response({'message':'success'}, status = 200)

def like__check(username, post__id):
    try:
        tempt = like_check.objects.get(user_name = username, post_id = post__id)
        return 0
    except:
        return 1

@api_view(['POST'])
def content_view(request):
    post__id = request.data.get('id')
    user_name = request.user.username
    tempt = post.object.get(id = post__id)
    rtr = {}
    rtr['content'] = tempt.content
    rtr['title'] = tempt.title
    rtr['author'] = tempt.author
    rtr['watch'] = tempt.watch
    rtr['year'] = tempt.year
    rtr['month'] = tempt.month
    rtr['like'] = tempt.like
    rtr['like_check'] = like__check(user_name, post__id)
    rtr['day'] = tempt.day
    rtr['hour'] = tempt.hour
    rtr['minute'] = tempt.minute
    rtr['comment'] = []
    tempt_comment = comment.objects.filter(post_id = post__id)
    for tmp in tempt_comment:
        rtr['comment'].append({'content' : tmp.content, 'author' : tmp.author,'year':tmp.year,'month':tmp.month,'day':tmp.day,'hour':tmp.hour,'minute':tmp.minute})
    return rtr


@api_view(['POST'])
def post_view(request):
    rtr = {}
    rtr['free'] = []
    rtr['popular'] = []
    tempt1 = {'id' : 1,'author' : 'minju','title' : 'sibal','watch' : 10,'year' : 2024,'month' : 5,'day' : 34, 'comment_number' : 3, 'content' : "WHOWWO"}
    tempt2 = {'id' : 2,'author' : 'minju','title' : 'sibal','watch' : 10,'year' : 2024,'month' : 5,'day' : 34, 'comment_number' : 3, 'content' : "WHOWWO"}
    tempt3 = {'id' : 3,'author' : 'minju','title' : 'sibal','watch' : 10,'year' : 2024,'month' : 5,'day' : 34, 'comment_number' : 3, 'content' : "WHOWWO"}
    tempt4 = {'id' : 4,'author' : 'minju','title' : 'sibal','watch' : 10,'year' : 2024,'month' : 5,'day' : 34, 'comment_number' : 3, 'content' : "WHOWWO"}
    tempt5 = {'id' : 5,'author' : 'minju','title' : 'sibal','watch' : 10,'year' : 2024,'month' : 5,'day' : 34, 'comment_number' : 3, 'content' : "WHOWWO"}
    tempt6 = {'id' : 6,'author' : 'minju','title' : 'sibal','watch' : 10,'year' : 2024,'month' : 5,'day' : 34, 'comment_number' : 3, 'content' : "WHOWWO"}
    tempt7 = {'id' : 7,'author' : 'minju','title' : 'sibal','watch' : 10,'year' : 2024,'month' : 5,'day' : 34, 'comment_number' : 3, 'content' : "WHOWWO"}
    tempt8 = {'id' : 8,'author' : 'minju','title' : 'sibal','watch' : 10,'year' : 2024,'month' : 5,'day' : 34, 'comment_number' : 3, 'content' : "WHOWWO"}
    rtr['free'].append(tempt1)
    rtr['free'].append(tempt2)
    rtr['free'].append(tempt5)
    rtr['free'].append(tempt6)
    rtr['popular'].append(tempt3)
    rtr['popular'].append(tempt4)
    rtr['popular'].append(tempt7)
    rtr['popular'].append(tempt8)
    return Response(rtr, status = 200)