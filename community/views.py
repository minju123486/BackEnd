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
from .models import post, comment, like_check, grade_search

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
    post_1 = post.objects.get(id=post_id)
    post_1.like += 1
    post_1.save()
    return Response({'message':'success'}, status = 200)


@api_view(['POST'])   
def post_dislike(request): # for professor
    post_id = request.data.get('id')
    post_1 = post.objects.get(id=post_id)
    post_1.like -= 1
    post_1.save()
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
    print(post__id)
    user_name = request.user.username
    print(3)
    tempt = post.objects.get(id = post__id)
    tempt.watch += 1
    tempt.save()
    print(4)
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
    for i in range(1,5):
        tempt_grade_search = grade_search.objects.filter(grade=str(i))
        tmp_lst = []
        for tmp in tempt_grade_search:
            w,g,c = tmp.watch, tmp.grade, tmp.content
            tmp_lst.append((w,g,c))
        sorted_data_Bysearch = sorted(tmp_lst, key=lambda x: (x[0]), reverse=True)
        rtr[str(i)] = sorted_data_Bysearch
    return Response(rtr, status = 200)


@api_view(['POST'])
def post_view(request):
    rtr = {}
    lst = []
    all_posts = post.objects.all()
    for tmp in all_posts:
        lst.append({'id':tmp.id,'title' : tmp.title, 'author' : tmp.author, 'content':tmp.content, 'year':tmp.year, 'month':tmp.month, 'day':tmp.day,'hour':tmp.hour,'minute':tmp.minute, 'watch':tmp.watch, 'like':tmp.like, 'comment_number':tmp.comment_number})
    sorted_data_Byfree = sorted(lst, key=lambda x: (x['year'], x['month'], x['day'], x['hour'], x['minute']), reverse=True)
    sorted_data_Bywatch = sorted(lst, key=lambda x: (x['watch']), reverse=True)
    while len(sorted_data_Bywatch) > 4:
        sorted_data_Bywatch.pop()
    rtr['free'] = sorted_data_Byfree
    rtr['popular'] = sorted_data_Bywatch
    print(rtr['free'])
    print(rtr['popular'])

    return Response(rtr, status = 200)

@api_view(['POST'])
def search(request):
    rtr = {}
    lst = []
    all_posts = post.objects.all()
    inp = request.data.get('content')
    print(inp)
    for tmp in all_posts:   
        if inp in tmp.title or inp in tmp.content:
            lst.append({'id':tmp.id,'title' : tmp.title, 'author' : tmp.author, 'content':tmp.content, 'year':tmp.year, 'month':tmp.month, 'day':tmp.day,'hour':tmp.hour,'minute':tmp.minute, 'watch':tmp.watch, 'like':tmp.like, 'comment_number':tmp.comment_number})
    sorted_data_Bysearch = sorted(lst, key=lambda x: (x['year'], x['month'], x['day'], x['hour'], x['minute']), reverse=True)
    rtr['search'] = sorted_data_Bysearch
    print(rtr['search'])
    try:
        obj = grade_search.objects.get(grade = request.user.grade, content = inp)
        obj.watch += 1
        obj.save()
    except:
        obj = grade_search.objects.get(grade = request.user.grade, content = inp, watch = 1)
        obj.save()
        

    return Response(rtr, status = 200)

@api_view(['POST'])   
def comment_create(request): # for professor
    post__id = request.data.get('post_id')
    post_author = 'hahahahaaha'
    post_content = request.data.get('content')
    print(post__id, post_author, post_content)
    now = datetime.now()


    n_year = now.year
    n_month = now.month
    n_day = now.day
    n_hour = now.hour
    n_minute = now.minute
    tempt = comment(post_id = post__id, content = post_content, author = post_author, year = n_year, month = n_month, day = n_day, hour = n_hour, minute = n_minute)
    tempt.save()
    return Response({'message':'success'}, status = 200)


