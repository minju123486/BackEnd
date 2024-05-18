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
from .models import post, comment

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


@api_view(['POST'])
def content_view(request):
    post__id = request.data.get('id')
    tempt = post.object.get(id = post__id)
    rtr = {}
    rtr['content'] = 'content'
    rtr['title'] = 'content'
    rtr['author'] = 'content'
    rtr['watch'] = 4
    rtr['year'] = 2024
    rtr['month'] = 11
    rtr['like'] = 1
    rtr['like_check'] = 0
    rtr['day'] = 24
    rtr['hour'] = 17
    rtr['minute'] = 17
    rtr['comment'] = []
    rtr['comment'].append({'content' : 'content', 'author' : 'author','year':2024,'month':5,'day':18,'hour':17,'minute':52})
    rtr['comment'].append({'content' : 'content', 'author' : 'author','year':2024,'month':5,'day':18,'hour':17,'minute':52})
    return rtr