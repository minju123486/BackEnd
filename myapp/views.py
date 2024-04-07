from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render 
from django.http import JsonResponse
from myapp import gpt_prompt
import openai
import os
# from django.conf import settings

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', './capde.settings.py')
# settings.configure()

user_data = dict()


openai.api_key = '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'

history = []
def get_completion(prompt):     
    history.append({'role':'user','content':gpt_prompt.prompt_1}) 
    query = openai.ChatCompletion.create( 
       model="gpt-4",
       messages=[{"role": "system", "content": gpt_prompt.Short_answer_message}, {'role':'user','content':gpt_prompt.prompt_4}], 
       max_tokens=1024, 



       n=1,
       stop=None,
       temperature=0.5, 
    ) 
    response = query.choices[0].message["content"]
    history.append({'role':'assistant', 'content':response})
    print(response)
    return response

def index(request):
    return HttpResponse("Communication start")
    
def query_view(request): 
    prompt = request.data.get('username') 
    prompt=str(prompt)
    response = get_completion(prompt)
    return JsonResponse({'response': response}), response 

@api_view(['POST'])
def login_view(request):
    global user_data
    username = request.data.get('username')
    password = request.data.get('password')
    check = True
    print(username)
    a, tmp= query_view(request)
    print()
    print(a)
    if username not in user_data:
        user_data[username] = password
        check = True
    else:
        check = False
        
    if check:
        # �α��� ���� ó��
        return Response({'message': 'Success'}, status=status.HTTP_200_OK)
    else:
        # �α��� ���� ó��
        return Response({'message': 'Fail'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def GenerateWriteProblem(request):
    a, tmp = query_view(request)
    lst = list(tmp.split("\n"))
    rtr = []
    check = False
    tempt = dict()
    for i in lst:
        if check:
            id = 0
            while i[id] == ' ' or i[id] == '.' or i[id] == '1' or i[id] == '2' or i[id] == '3' or i[id] == '4':
                id += 1 
            tempt['question'] = i[id::]
            rtr.append(tempt)
            tempt = dict()
            check = False
            continue
        if i[0:2] == '문제':
            if len(i) == 2:
                check = True
                continue
            else:
                id = 2
                while id <len(i) and i[id] == ' ':
                    id += 1
                if len(i) == id:
                    check = True
                    continue
                b = i[id::]
                tempt['question'] = b
                rtr.append(tempt)
                tempt = dict()
    print(rtr)
    return Response(rtr, status=status.HTTP_200_OK)
                

@api_view(['POST'])
def GenerateMultipleProblem(request):
    a, tmp = query_view(request)
    lst = list(tmp.split("\n"))
    rtr = []
    check = False
    idx = 1
    tempt = dict()
    for i in lst:
        if check:
            id = 0
            while i[id] == ' ' or i[id] == '.' or i[id] == '1' or i[id] == '2' or i[id] == '3' or i[id] == '4':
                id += 1 
            tempt['question'] = i[id::]
            check = False
            continue
        if i[0:2] == '문제':
            if len(i) == 2:
                check = True
            else:
                id = 2
                while id <len(i) and i[id] == ' ':
                    id += 1
                if len(i) == id:
                    check = True
                    continue
                b = i[id::]
                tempt['question'] = b
                tempt['options'] = []
        elif len(i) > 0 and i[0]!= '-' and i[0] != ' ' and i[0:2] != '정답' and 1 <= int(i[0]) <= 4:
            b = i[4:]
            tempt['options'].append(b)
        elif i[0:2] == '정답':
            tempt['answer'] = i
            for j in i:
                if i == '1' or i == '2' or i == '3' or i == '4' :tempt['answer_number'] = int(i)
            rtr.append(tempt)
            tempt = dict()
            continue
    print(rtr)
    return Response(rtr, status=status.HTTP_200_OK)