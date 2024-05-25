from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
import os
import environ
import requests
import json
from langchain_community.chat_models.friendli import ChatFriendli
import deepl
from rest_framework.permissions import IsAuthenticated
user_data = dict()

from pathlib import Path
from django.shortcuts import render 
from django.http import JsonResponse
from myapp import gpt_prompt
from openai import OpenAI
import os
from .models import course, professor_lecture, student_lecture, problem, answer, feedback_list
from Login.models import school
from .crawling import crawl_lst
from datetime import datetime
# env = environ.Env()
# environ.Env.read_env(Path(__file__).resolve().parent/'.env')
# openai.api_key = env('Key')
client = OpenAI(
    # This is the default and can be omitted
    api_key= "sk-proj-G1C3bQtNGqVvdo1dfu4IT3BlbkFJaWHW58ubXnAR3vlaNbqK"
)
Sub_dict = {"Java" : 1, "C++" : 2, "Python" : 3}
llll = {"자바프로그래밍-Arrays" : "luXuJcSJIcw5", "자바프로그래밍-Class Definitions" : "a41ZG0hk2twJ", "자바프로그래밍-Classes in Depth 1" : "BbiOoy98Wyi5", "자바프로그래밍-Classes in Depth 2" : "sWGgKi5KqCa6", "자바프로그래밍-Conditional Statements" : "ISsjFKdItU7p", "자바프로그래밍-Constructors" : "yowiRGZTt6jd", "자바프로그래밍-Control Statements" : "ZqOtWYcaHo6P", "자바프로그래밍-Creating Objects" : "kkoVuywBXCNa", "자바프로그래밍-Data Types" : "b2hWgyTmqimV", "자바프로그래밍-Inheritance" : "hFZn6DiEgJkZ", "자바프로그래밍-Iteration Statements" : "es7n8OVm1PnO", "자바프로그래밍-Operators" : "WUY7Xkj41TJi", "자바프로그래밍-Overriding" : "EndmGmlEqpsq", "자바프로그래밍-Using Objects" : "oH6BmXs9m6RP", "C++프로그래밍-Constructors" : "3u69DmLLf5Hb", "C++프로그래밍-arithmetic operators" : "F44nLRsiqydg", "C++프로그래밍-Destructors" : "zCjoBh6iNVCn", "C++프로그래밍-Function Overloading" : "S2LwTGWcgHGU", "C++프로그래밍-Functions" : "4DKNfTAxbLoM", "C++프로그래밍-Inheritance" : "1JgbN6hi14Ik", "C++프로그래밍-Iteration statements" : "3KFCsIq9OMxV", "C++프로그래밍-pointer new and delete operators" : "orgeg9QPujko", "C++프로그래밍-Pointer operators" : "QBZrZ4Ze9DgC", "C++프로그래밍-Selection statements (if-else statements)" : "pUo77VMoVrWU", "C++프로그래밍-shared_ptr" : "TaWAtTe8JNZb", "C++프로그래밍-smart pointers" : "JSTucnFuIwtc", "C++프로그래밍-String and Character Literals" : "lREJrk9fil2E", "C++프로그래밍-unique_ptr" : "hVR275pTMInf", "파이썬프로그래밍-A Brief Introduction to Python" : "EtXRJAytipFQ", "파이썬프로그래밍-Classes" : "Mjqb8EhhRLdb", "파이썬프로그래밍-Data Structure" : "jtEYJ29v4zA5", "파이썬프로그래밍-Errors and Exceptions" : "G4zOpdHNBlJA", "파이썬프로그래밍-Input and Output" : "aegIWPDWEjGZ", "파이썬프로그래밍-Modules" : "sp0hbuD6Uez3", "파이썬프로그래밍-Other Control Flow Tools" : "3fA5ueffMiNH", "파이썬프로그래밍-Standard Library Quick Look - Part 2" : "q2PhVusiIitU", "파이썬프로그래밍-Standard Library Quick Look" : "miclvsK4ZpjF", "파이썬프로그래밍-Using the Python Interpreter" : "nzeu0Ypmodfl", "파이썬프로그래밍-Virtual Environments and Packages" : "2LI0V1foae43"}

Quest_dict = {'객관식-빈칸': 1, '객관식-단답형': 2, '객관식-문장형': 3, '단답형-빈칸': 4, '단답형-문장형': 5, 'OX선택형-O/X': 6, '서술형-코딩': 7}
history = []
def get_completion(prompt, numberKey,count, subject, rags, tempt_problem):     
    history.append({'role':'user','content':gpt_prompt.prompt_lst[numberKey](count,subject, rags, tempt_problem)}) 
    query = client.chat.completions.create( 
       model="gpt-4-turbo",
       messages=[{"role": "system", "content": gpt_prompt.System_lst[numberKey]}, {'role':'user','content':gpt_prompt.prompt_lst[numberKey](count,subject, rags, tempt_problem)}], 
       max_tokens=1028, 
    ) 
    response = query.choices[0].message.content
    history.append({'role':'assistant', 'content':response})
    print(response)
    return response

def chat_function(message):
    new_messages = []
    auth_key = "44c49157-0a84-4b83-954f-1b9125baf794:fx"
    llm = ChatFriendli(
    model="meta-llama-3-70b-instruct", friendli_token="flp_OydC1Y4tVFBfs1cgI5u0h9bUkQnNDrROcj3ARS751k083"
)

    new_messages.append({"role": "user", "content": message})

    response = llm.invoke(new_messages)
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(response.content, target_lang="KO")
    return result.text



def friend_completion(prompt, numberKey,count, subject, rags, tempt_problem): 
    url = "https://suite.friendli.ai/api/beta/retrieve"

    PAT = "flp_OydC1Y4tVFBfs1cgI5u0h9bUkQnNDrROcj3ARS751k083"

    payload = json.dumps({
    "query": "Give me 5 multiple choice questions",
    "k": 13,
    "document_ids": [rags]
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {PAT}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response = response.json()
    contexts = [r["content"] for r in response["results"]]

    llm = ChatFriendli(
        model="meta-llama-3-70b-instruct", friendli_token="flp_OydC1Y4tVFBfs1cgI5u0h9bUkQnNDrROcj3ARS751k083"
    )


    template = """{sys_message}
    {context}

    Question: {question}

    Helpful Answer:"""

    rag_message = template.format(sys_message = gpt_prompt.System_lst[numberKey],
        context="\n".join(contexts), question=gpt_prompt.prompt_lst[numberKey](count,subject, rags, tempt_problem)
    )
    auth_key = "44c49157-0a84-4b83-954f-1b9125baf794:fx"
    translator = deepl.Translator(auth_key)

    message = llm.call_as_llm(message=rag_message)
    client = OpenAI(
    api_key="up_n76I9G4SKzOq3N463RI0V2x3r7d6n",
    base_url="https://api.upstage.ai/v1/solar"
    )
    content = message

    stream = client.chat.completions.create(
    model="solar-1-mini-translate-enko",
    messages=[
        {
        "role": "user",
        "content": "Father went into his room"
        },
        {
        "role": "assistant",
        "content": "아버지가방에들어가셨다"
        },
        {
        "role": "user",
        "content": content
        }
    ],
    stream=True,
    )
    rtr = ''
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            rtr += chunk.choices[0].delta.content
    print(rtr)
    return rtr
    
def query_view(request,numberKey, count, subject, rags, tempt_problem): 
    prompt = request.data.get('username') 
    prompt=str(prompt)
    response = get_completion(prompt, numberKey,count, subject, rags, tempt_problem)
    return JsonResponse({'response': response}), response 

def index(request):
    return HttpResponse("Communication start")

def get_completion_feedback(prompt):     
    query = client.chat.completions.create( 
       model="gpt-4",
       messages=[{"role": "system", "content": gpt_prompt.sys_feedback}, {'role':'user','content': prompt}], 
       max_tokens=1024
    ) 
    response = query.choices[0].message.content
    print(response)
    return response

def query_view_feedback(request, prompt):  
    prompt=str(prompt)
    response = get_completion_feedback(prompt)
    return JsonResponse({'response': response}), response 


def GenerateWriteProblem(tmp):
    lst = list(tmp.split("\n"))
    rtr = []
    check = False
    tempt = dict()
    for i in lst:
        if check:
            id = 0
            while i[id] == ' ' or i[id] == '.' or i[id] == '1' or i[id] == '2' or i[id] == '3' or i[id] == '4':
                id += 1 
            tempt['content'] = i[id::]
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
                tempt['content'] = b
        if i[0:7] == 'problem':
            if len(i) == 7:
                check = True
                continue
            else:
                id = 7
                while id <len(i) and i[id] == ' ':
                    id += 1
                if len(i) == id:
                    check = True
                    continue
                b = i[id::]
                tempt['content'] = b
        elif i[0:2] == '정답' or i[0:2] == '정닱':
            tempt['answer'] = i[4::]
            rtr.append(tempt)
            tempt = dict()
        elif i[0:6] == 'Answer':
            tempt['answer'] = i[8::]
            rtr.append(tempt)
            tempt = dict()
    # print(rtr)
    return rtr
            
def GenerateMultipleProblem(tmp):
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
            tempt['content'] = i[id::]
            tempt['options'] = []
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
                tempt['content'] = b
                tempt['options'] = []
        if i[0:7] == 'problem':
            if len(i) == 7:
                check = True
            else:
                id = 7
                while id <len(i) and i[id] == ' ':
                    id += 1
                if len(i) == id:
                    check = True
                    continue
                b = i[id::]
                tempt['content'] = b
                tempt['options'] = []
        elif len(i) > 0 and i[0]!= '-' and i[0] != ' ' and i[0:2] != '정답' and i[0:2] != '정닱'  and i[1] == '.' and 1 <= int(i[0]) <= 4:
            b = f'{i[0]}번 : {i[4:]}'
            tempt['options'].append(b)
        elif i[0:2] == '정답' or i[0:2] == '정닱':
            tt = ''
            ch = 0
            ttt = 0
            for j in i:
                if ch == 3:
                    tt += j
                if ch == 1 or ch == 2:
                    ch += 1
                    continue
                if j == '1' or j == '2' or j == '3' or j == '4' :
                    ttt = int(j)
                    ch = 1
            tempt['answer'] = f'정답 : {ttt}번  {tt}'
            rtr.append(tempt)
            tempt = dict()
            continue
        elif i[0:6] == 'Answer':
            tt = ''
            ch = 0
            ttt = 0
            for j in i:
                if ch == 12:
                    tt += j
                if ch < 12:
                    ch += 1
                    continue
                if j == '1' or j == '2' or j == '3' or j == '4' :
                    ttt = int(j)
                    ch = 1
            tempt['answer'] = f'정답 : {ttt}번  {tt}'
    # print(rtr)
    return rtr

def Code_problem(tmp):
    lst = list(tmp.split("\n"))
    rtr = []
    check = False
    idx = 1
    tempt = dict()
    toggle = True
    quest = ''
    for i in lst:
        if check:
            id = 0
            if len(i) == 0:
                continue
            while i[id] == ' ' or i[id] == '.' or i[id] == '1' or i[id] == '2' or i[id] == '3' or i[id] == '4':
                id += 1 
                
            quest += i[id::]+'\n'
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
                b = i[id::]+'\n'
                quest += b
        elif i[0:3] == '```':
            if toggle == True:
                tempt['language'] = i[3::]
                toggle = False
            else:
                tempt['content'] = quest
                quest = ''
                toggle = True
                rtr.append(tempt)
                tempt = dict()
        elif not toggle:
            quest += i+'\n'
    # print(rtr)
    return rtr
            
@api_view(['POST'])
def GenerateQuestion(request):
    global llll
    print(request.data.get('selections'))
    
    ans = {}
    ans['questions'] = []
    problem_lst = []
    coursename = request.data.get('course_name') # course name 가져오기
    # lectureid = request.data.get('lecture_id') # course name 가져오기
    keyword = request.data.get('selectedKeywords') # course name 가져오기
    rags = llll[coursename+'-'+keyword[0]]
    professor_user_name = request.user.username # professor username 가져오기
    professor_user_id = request.user.id # professor username 가져오기
    for _ in range(10):
        problem_lst.append('')
    cnt = 0
    tempt_problem = ''
    for m in range(1,8):
        for tempt in request.data.get('selections'):    
            if 1 <= Quest_dict[tempt] <= 3 and m == Quest_dict[tempt]:
                tmp = dict()
                tmp['type'] = Quest_dict[tempt]
                t = friend_completion(request,Quest_dict[tempt], request.data.get('selections')[tempt], coursename, rags, tempt_problem)
                tmp['items'] = GenerateMultipleProblem(t)
                tmp['count'] = request.data.get('selections')[tempt]
                c = request.data.get('selections')[tempt]
                ans['questions'].append(tmp)
                for k in tmp['items']:
                    tempt_content = f'{Quest_dict[tempt]}'
                    for i in k:
                        if i == 'content':
                            tempt_problem += k[i]+'\n'
                        elif i == 'options':
                            for id, j in enumerate(k[i]):
                                tempt_problem += '' #f'{id+1}번 : ' +'\n'
                        elif i == 'answer':
                            tempt_problem +='' # k[i]+'\n'
                    tempt_problem += '\n'
            elif 4 <= Quest_dict[tempt] <= 6 and m == Quest_dict[tempt]:
                tmp = dict()
                tmp['type'] = Quest_dict[tempt]
                a, t = query_view(request,Quest_dict[tempt], request.data.get('selections')[tempt], coursename, rags, tempt_problem)
                tmp['items'] = GenerateWriteProblem(t)
                tmp['count'] = request.data.get('selections')[tempt]
                c = request.data.get('selections')[tempt]
                ans['questions'].append(tmp)
                for k in tmp['items']:
                    tempt_content = f'{Quest_dict[tempt]}'
                    for i in k:
                        if i == 'content':
                            tempt_problem += k[i]+'\n'
                        elif i == 'answer':
                            tempt_problem +='' #k[i]+'\n'
                    tempt_problem += '\n'
                    cnt += 1
            elif Quest_dict[tempt] == 7 and m == Quest_dict[tempt]:
                tmp = dict()
                tmp['type'] = Quest_dict[tempt]
                a, t = query_view(request,Quest_dict[tempt], request.data.get('selections')[tempt])
                tmp['items'] = Code_problem(t)
                tmp['count'] = request.data.get('selections')[tempt]
                ans['questions'].append(tmp)
                problem_lst.append(t)
    print(problem_lst)
    lecture = professor_lecture.objects.filter(course_name=coursename, username=professor_user_name).first()
    print(lecture)
    print('-------------------------------------------')
    print(tempt_problem)
    print('-------------------------------------------')
    print(professor_user_name)
    print(ans)
    return Response(ans, status=status.HTTP_200_OK)


@api_view(['POST'])
def problem_save(request):  
    print(request.data.get('questions'))
    coursename = request.data.get('course_name')
    professor_user_name = request.user.username
    professor_user_id = request.user.id
    lecture = professor_lecture.objects.filter(course_name=coursename, username=professor_user_name).first()
    print(professor_user_name, coursename, ' 문제 저장')
    problem_lst = []
    for _ in range(10):
        problem_lst.append("")
    tempt_problem = problem.objects.filter(lecture_id = lecture.id, professor_id = professor_user_id)
    if tempt_problem.exists():
        tempt_problem.delete()
    count = 0
    for i in range(1,8):
        for t in request.data.get('questions'):
            if t['type'] == i and (i == 1 or  i == 2 or i == 3):
                for item in t['items']:
                    tempt = str(t['type']) + "$$"
                    tempt += (item['content'] + "$$")
                    for opt in item['options']:
                        tempt += (opt + "$$")
                    tempt += (item['answer'] +"$$")
                    tempt += str(t['count'])
                    problem_lst[count] = tempt
                    count += 1
            if t['type'] == i and (i == 4 or i == 5 or i == 6):
                for item in t['items']:
                    tempt = str(t['type']) + "$$"
                    tempt += (item['content'] + "$$")
                    tempt += (item['answer'] +"$$")
                    tempt += str(t['count'])
                    problem_lst[count] = tempt
                    count += 1
    print(problem_lst)
    obj = problem(problem_1 = problem_lst[0], problem_2 = problem_lst[1] , problem_3 = problem_lst[2], problem_4 = problem_lst[3], problem_5 = problem_lst[4], problem_6 = problem_lst[5], problem_7 = problem_lst[6], problem_8 = problem_lst[7], problem_9 = problem_lst[8], problem_10 = problem_lst[9], lecture_id = lecture.id , professor_id = professor_user_id)
    obj.save()
    return Response({"message":"success"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def student_problem(request):
    print(request.data)
    coursename = request.data.get('course_name')
    professor_name = request.data.get('course_professor')
    print(professor_name, coursename)
    obj = school.objects.filter(username = professor_name).first()
    professor_id = obj.id
    lecture = professor_lecture.objects.filter(username = professor_name, course_name = coursename).first()
    lecture__id = lecture.id
    tempt_problem = problem.objects.filter(lecture_id = lecture__id, professor_id = professor_id).first()
    problem_lst = [tempt_problem.problem_1, tempt_problem.problem_2, tempt_problem.problem_3, tempt_problem.problem_4, tempt_problem.problem_5, 
                   tempt_problem.problem_6, tempt_problem.problem_7, tempt_problem.problem_8 ,tempt_problem.problem_9 ,tempt_problem.problem_10]
    while problem_lst[len(problem_lst)-1] == '':
        problem_lst.pop()
    rtr = {'questions':[]}
    dic = dict()
    for i in problem_lst:
        dic[i[0]] = 1
    print(dic)
    for m in dic:
        tempt = {}
        tempt['type'] = int(m)
        tempt['items'] = []
        check = 0
        for k in problem_lst:
            if int(k[0]) != int(m):
                continue
            check = 1
            tempt['count'] = int(k[len(k)-1])
            lst = list(k.split("$$"))
            tmp = {}
            if lst[0] == '1' or lst[0] == '2' or lst[0] == '3':
                tmp['content'] = lst[1]
                tmp['options'] = []
                tmp['options'].append(lst[2])
                tmp['options'].append(lst[3])
                tmp['options'].append(lst[4])
                tmp['options'].append(lst[5])
                tmp['answer'] = lst[6]
            elif lst[0] == '4' or lst[0] == '5' or  lst[0] == '6':
                tmp['content'] = lst[1]
                tmp['answer'] = lst[2]
            tempt['items'].append(tmp)
        if check == 1:
            rtr['questions'].append(tempt)
    print(rtr)
    return Response(rtr, status=status.HTTP_200_OK)
                
                
@api_view(['POST'])
def feedback_problem(request):
    print(request.data)
    coursename = request.data.get('course_name')
    professor_name = request.data.get('course_professor')
    obj = school.objects.filter(username = professor_name).first()
    professor_id = obj.id
    lecture = professor_lecture.objects.filter(username = professor_name, course_name = coursename).first()
    lecture__id = lecture.id
    tempt_problem = problem.objects.filter(lecture_id = lecture__id, professor_id = professor_id).first()
    problem_lst = [tempt_problem.problem_1, tempt_problem.problem_2, tempt_problem.problem_3, tempt_problem.problem_4, tempt_problem.problem_5, 
                   tempt_problem.problem_6, tempt_problem.problem_7, tempt_problem.problem_8 ,tempt_problem.problem_9 ,tempt_problem.problem_10]
    while problem_lst[len(problem_lst)-1] == '':
        problem_lst.pop()
    rtr = {'questions':[]}
    dic = dict()
    for i in problem_lst:
        dic[i[0]] = 1
    print(dic)
    for m in dic:
        tempt = {}
        tempt['type'] = int(m)
        tempt['items'] = []
        check = 0
        for k in problem_lst:
            if int(k[0]) != int(m):
                continue
            check = 1
            tempt['count'] = int(k[len(k)-1])
            lst = list(k.split("$$"))
            tmp = {}
            if lst[0] == '1' or lst[0] == '2' or lst[0] == '3':
                tmp['content'] = lst[1]
                tmp['options'] = []
                tmp['options'].append(lst[2])
                tmp['options'].append(lst[3])
                tmp['options'].append(lst[4])
                tmp['options'].append(lst[5])
                tmp['answer'] = lst[6]
            elif lst[0] == '4' or lst[0] == '5' or  lst[0] == '6':
                tmp['content'] = lst[1]
                tmp['answer'] = lst[2]
            tempt['items'].append(tmp)
        if check == 1:
            rtr['questions'].append(tempt)
    print(rtr)
    return Response(rtr, status=status.HTTP_200_OK)
        
@api_view(['POST'])
def student_answer(request):
    coursename = request.data.get('course_name')
    professor_name = request.data.get('course_professor')
    l_answer_1 = request.data.get('answers')['answer1']
    l_answer_2 = request.data.get('answers')['answer2']
    l_answer_3 = request.data.get('answers')['answer3']
    l_answer_4 = request.data.get('answers')['answer4']
    l_answer_5 = request.data.get('answers')['answer5']
    l_answer_6 = request.data.get('answers')['answer6']
    l_answer_7 = request.data.get('answers')['answer7']
    l_answer_8 = request.data.get('answers')['answer8']
    l_answer_9 = request.data.get('answers')['answer9']
    l_answer_10 = request.data.get('answers')['answer10']
    l_answer_lst = [l_answer_1,l_answer_2,l_answer_3,l_answer_4,l_answer_5,l_answer_6,l_answer_7,l_answer_8,l_answer_9,l_answer_10]
    print(l_answer_lst)
    while l_answer_lst[len(l_answer_lst)-1] == '':
        l_answer_lst.pop()
    print(l_answer_lst)
    obj = professor_lecture.objects.filter(username = professor_name, course_name = coursename).first()
    tmp = answer.objects.filter(lecture_id = obj.id , student_id = request.user.id)
    if tmp.exists():
        tmp.delete()
    tempt = answer(answer_1 = l_answer_1, answer_2 = l_answer_2 , answer_3 = l_answer_3, answer_4 = l_answer_4, answer_5 = l_answer_5, answer_6 = l_answer_6, answer_7 = l_answer_7, answer_8 = l_answer_8, answer_9 = l_answer_9, answer_10 = l_answer_10, lecture_id = obj.id , student_id = request.user.id)
    tempt.save()
    return Response({'message':'success'}, status = 200)
    
@api_view(['POST'])
def problem_check(request):
    professor_name = request.data.get('professor_name')
    course_name = request.data.get('course_name')
    lecture_tempt = professor_lecture.objects.filter(username = professor_name, course_name = course_name).first()
    try:
        lecture__id = lecture_tempt.id
        pl = problem.objects.get(lecture_id = lecture__id).first()
        return Response({'check':1}, status=status.HTTP_200_OK)
    except:
        return Response({'check':0}, status=status.HTTP_200_OK)
    
@api_view(['POST'])   
def feedback(request): # for professor
    idx = request.data.get('id')
    print('--------------------------')
    print(idx)
    print('--------------------------')
    lecture_tempt = feedback_list.objects.filter(id = idx).first()
    rtr = {}
    lst = list(lecture_tempt.correct_count.split(" "))
    for i in range(1,len(lst)+1):
        rtr[str(i)] = lst[i-1]
    rtr['count'] = lecture_tempt.count
    rtr['cnt'] = lecture_tempt.cnt
    rtr['feedback'] = lecture_tempt.feedback
    problem_lst = [lecture_tempt.problem_1, lecture_tempt.problem_2, lecture_tempt.problem_3, lecture_tempt.problem_4, lecture_tempt.problem_5, 
                lecture_tempt.problem_6, lecture_tempt.problem_7, lecture_tempt.problem_8 ,lecture_tempt.problem_9 ,lecture_tempt.problem_10]
    while problem_lst[len(problem_lst)-1] == '':
        problem_lst.pop()
    rtr['questions'] = []
    dic = dict()
    for i in problem_lst:
        dic[i[0]] = 1
    print(dic)
    for m in dic:
        tempt = {}
        tempt['type'] = int(m)
        tempt['items'] = []
        check = 0
        for k in problem_lst:
            if int(k[0]) != int(m):
                continue
            check = 1
            tempt['count'] = int(k[len(k)-1])
            lst = list(k.split("$$"))
            tmp = {}
            if lst[0] == '1' or lst[0] == '2' or lst[0] == '3':
                tmp['content'] = lst[1]
                tmp['options'] = []
                tmp['options'].append(lst[2])
                tmp['options'].append(lst[3])
                tmp['options'].append(lst[4])
                tmp['options'].append(lst[5])
                tmp['answer'] = lst[6]
            elif lst[0] == '4' or lst[0] == '5' or  lst[0] == '6':
                tmp['content'] = lst[1]
                tmp['answer'] = lst[2]
            tempt['items'].append(tmp)
        if check == 1:
            rtr['questions'].append(tempt)
    print(rtr)
    return Response(rtr, status=status.HTTP_200_OK)

@api_view(['POST'])   
def feedback_view(request): # for professor
    professor_name = request.data.get('course_professor')
    course_name = request.data.get('course_name')
    print(professor_name)
    print(course_name)
    feedback_tempt = feedback_list.objects.filter(username = professor_name, coursename = course_name)
    rtr = {}
    rtr['date'] = []
    rtr['id'] = []
    for k in feedback_tempt:
        tempt = {}
        dat = f'{k.year}.{k.month}.{k.day}.'
        rtr['date'].append(dat)
        rtr['id'].append(k.id)
    print(rtr)
    return Response(rtr, status=status.HTTP_200_OK)


@api_view(['POST'])   
def feedback_save(request): # for professor
    professor_name = request.data.get('professor_name')
    course_name = request.data.get('course_name')
    lecture_tempt = professor_lecture.objects.filter(username = professor_name, course_name = course_name).first()
    print(lecture_tempt.course_name)
    lecture__id = lecture_tempt.id
    pl = problem.objects.filter(lecture_id = lecture__id).first()
    problem_lst = [pl.problem_1,pl.problem_2,pl.problem_3,pl.problem_4,pl.problem_5,pl.problem_6,pl.problem_7,pl.problem_8,pl.problem_9,pl.problem_10]
    now = datetime.now()


    n_year = now.year
    n_month = now.month
    n_day = now.day
    
    lst, feed_tempt, count, cnt = feed(request)
    
    tempt = feedback_list(username = professor_name, coursename = course_name, feedback = feed_tempt, year = n_year, month = n_month, day = n_day, count = count, cnt = cnt, correct_count = lst, problem_1 = problem_lst[0], problem_2 = problem_lst[1], problem_3 = problem_lst[2], problem_4 = problem_lst[3], problem_5 = problem_lst[4], problem_6 = problem_lst[5], problem_7 = problem_lst[6], problem_8 = problem_lst[7],problem_9 = problem_lst[8],problem_10 = problem_lst[9])
    tempt.save()
    problem.objects.filter(lecture_id = lecture__id).delete()
    answer.objects.filter(lecture_id = lecture__id).delete()
    return Response({'message':'success'}, status=status.HTTP_200_OK)

def feed(request): # for professor
    professor_name = request.data.get('professor_name')
    course_name = request.data.get('course_name')
    
    lecture_tempt = professor_lecture.objects.filter(username = professor_name, course_name = course_name).first()
    
    lecture__id = lecture_tempt.id 
    
    pl = problem.objects.filter(lecture_id = lecture__id).first()
    
    full_query = ''
    
    problem_lst = [pl.problem_1,pl.problem_2,pl.problem_3,pl.problem_4,pl.problem_5,pl.problem_6,pl.problem_7,pl.problem_8,pl.problem_9,pl.problem_10]
    while problem_lst[len(problem_lst)-1] == '':
        problem_lst.pop()
    count = len(problem_lst)
    for idx, pro in enumerate(problem_lst):
        lst = list(pro.split("$$"))
        if int(lst[0]) == 1 or int(lst[0]) == 2 or int(lst[0]) == 3:
            full_query += f'{idx+1} th question\n{lst[1]} \n {lst[2]} \n {lst[3]} \n {lst[4]} \n {lst[5]} \n answer : {lst[6]} \n'
        elif int(lst[0]) == 4 or int(lst[0]) == 5 or int(lst[0]) == 6:
            full_query += f'{idx+1} th question\n{lst[1]} \n answer : {lst[2]} \n'    
    obj = answer.objects.filter(lecture_id = lecture__id)
    
    full_query += '''\n The problems are as follows and now I will give you the answers of the students. Please give me feedback by summarizing all the answers. However, there are rules in the output and you must follow these rules.
                    Yes, I understand. Please give me only the necessary answers and exclude all the same answers.
                    First, tell me how many people got each problem right. Please tell me in the following format.
                    Problem number Number of people who got it right Please put only numbers without indicating the problem number and the number of people who got it right. Do not attach anything other than numbers.
                    Output for all problems in the same format as above and below that, write feedback on the students' understanding.
                    These are the problems I gave to check the students' understanding of the class content and it is enough to give feedback on where the understanding is lacking and where the understanding is good by summarizing the answers.
                    Since it is the first time that university undergraduate 1st and 2nd year students are learning, please judge it as correct if it is ambiguous and it is judged that it is understood to some extent.
                    You do not need to give feedback on each student individually, but give feedback after summarizing it as a whole.
                    Please give feedback by problem or by grouping similar contents. Please give detailed feedback assuming that it is viewed by a professional with at least a master's degree.
                    Please write only the feedback content without keywords such as 'Feedback :'.
                    '''
    cnt = len(obj)
    for idx, tempt in enumerate(obj):
        print(tempt)
        answer_lst = [tempt.answer_1,tempt.answer_2,tempt.answer_3,tempt.answer_4,tempt.answer_5,tempt.answer_6,tempt.answer_7,tempt.answer_8,tempt.answer_9,tempt.answer_10]
        while answer_lst[len(answer_lst)-1] == '':
            answer_lst.pop()
        tmp = f'{idx+1}th student answer \n\n'
        for idx,ans in enumerate(answer_lst):
            tmp += f'{idx+1} th question answer : {ans} \n'
        tmp += '\n\n'
        full_query += tmp
    print(full_query)
    answer_1 = chat_function(full_query)
    rtr = {}
    rtr_lst = list(answer_1.split("\n"))
    feed_tempt = ''
    lst = ''
    for k in rtr_lst:
        print(k)
        if len(k) >= 3 and len(k) <= 5:
            a,b = k.split(" ")
            lst += str(b)+' '
        else:
            feed_tempt += k
    rtr['feedback'] = feed_tempt
    rtr['count'] = count
    rtr['cnt'] = cnt
    print(rtr)
               
    # print(answer_1)
    return lst, feed_tempt, count, cnt             


@api_view(['POST'])
def mock_feedback(request):
    return Response({'date':['2024.05.12', '2024.05.31', '2024.05.14' ]}, status = 200)               
                    
                    
            
             
        

        
    
    
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_view(request):
    all_courses = course.objects.all()
    rtr = dict()
    rtr['lecture'] = []
    user_name = request.user.username
    print(f'course_view : for {user_name}')
    for i in all_courses:
        tempt = dict()
        tempt['key'] = i.id
        tempt['name'] = i.name
        obj = professor_lecture.objects.filter(username = user_name, course_name = i.name)
        print(obj)
        if not obj.exists():
            rtr['lecture'].append(tempt)
    # print(rtr)
    return Response(rtr, status=status.HTTP_200_OK)
    
@api_view(['GET'])    
def lecture_show(request): ## my 강의 
    id = request.user.id
    user_name = request.user.username
    lecture = professor_lecture.objects.filter(username = user_name)
    print(f'{user_name} 교수님 나의 강의 보기')
    if lecture.exists():
        rtr = dict()
        rtr['lecture'] = []
        for k in lecture:
            check = 0
            lecture__id = k.id
            tempt = problem.objects.filter(lecture_id = lecture__id)
            print("tempt", tempt)
            student_lec = student_lecture.objects.filter(lecture_id = lecture__id)
            answer_lec = answer.objects.filter(lecture_id = lecture__id)
            if tempt.exists():
                check = 1
            rtr['lecture'].append({'name':k.course_name, 'key':k.course_id, 'check':check,'count': len(student_lec),'student_count': len(answer_lec) })
        print(rtr)
        return Response(rtr, status = 200)
    else:
        return Response({}, status = 201) # 강의가 없는 경우
    
    
@api_view(['POST'])   
def lecture_generate(request): ## my 강의 
    try:
        user_name = request.user.username
        coursename = request.data.get('subject')
        print("교수 이름",user_name)
        tmp = professor_lecture.objects.filter(username = user_name, course_name = coursename)
        print(tmp)
        if tmp.exists():
            print("이미 있는 강의입니다.")
            return Response({'message':'This lecture is already'}, status = 422)
        
        obj = course.objects.filter(name = coursename).first()
        pl = professor_lecture.objects.create(username = user_name, course_name = coursename, course_id = obj.id, name = request.user.name)
        pl.save()
        return Response({'message':'success'}, status = 200)
    except:
        print("강의생성 되지않음")
        return Response({'message':'fail'}, status = 444)
    
    
    
@api_view(['GET'])
def lecture_view(request): # for student
    all_lecture = professor_lecture.objects.all()
    rtr = dict()
    rtr['lecture'] = []
    user_name = request.user.username
    for i in all_lecture:
        tempt = dict()
        tempt['course'] = i.course_name
        tempt['name'] = i.username
        tempt['professor'] = i.name # 실제이름
        tempt['lecture_id'] = i.id
        obj = student_lecture.objects.filter(username = user_name, course_name = i.course_name)
        print(obj)
        if not obj.exists():
            rtr['lecture'].append(tempt)
    print(rtr)
    return Response(rtr, status=status.HTTP_200_OK)


@api_view(['POST'])   
def lecture_apply(request): # for student
    try:
        user_name = request.user.username
        # user_name = request.user.username 나중에는 그냥 name 필요
        lecture_number = request.data.get('lecture_id')
        coursename = request.data.get('course')
        obj = course.objects.filter(name = coursename).first()
        sl = student_lecture.objects.create(username = user_name, course_name = coursename, course_id = obj.id, lecture_id = lecture_number, name = user_name) # name은 나중에 실제이름으로 대체
        sl.save()
        return Response({'message':'success'}, status = 200)
    except:
        print("강의신청 되지않음")
        return Response({'message':'fail'}, status = 444)
    
@api_view(['GET'])   
def my_lecture_show(request): # for student
    obj = student_lecture.objects.filter(username = request.user.username)
    rtr = dict()
    rtr['lecture'] = []
    for i in obj:
        check = 0
        tmp = professor_lecture.objects.filter(id = i.lecture_id).first()
        print("tmp",tmp)
        temporal_obj = school.objects.filter(username = tmp.username).first()
        tempt = problem.objects.filter(lecture_id = tmp.id, professor_id = temporal_obj.id)
        print("tempt", tempt)
        if tempt.exists():
            check = 1
        tempt = dict()
        tempt['course'] = i.course_name
        tempt['professor'] = tmp.username
        tempt['lecture_id'] = i.lecture_id
        tempt['check'] = check
        rtr['lecture'].append(tempt)
    print(rtr)
    return Response(rtr, status = 200)
    # return Response({'message':'fail'}, status = 444)/
    
    






