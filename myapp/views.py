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
from .models import course, professor_lecture, student_lecture, problem, answer
from Login.models import school
from .crawling import crawl_lst

# env = environ.Env()
# environ.Env.read_env(Path(__file__).resolve().parent/'.env')
# openai.api_key = env('Key')

Sub_dict = {"자바프로그래밍" : 1, "C++프로그래밍" : 2, "파이썬프로그래밍" : 3}


Quest_dict = {'객관식-빈칸': 1, '객관식-단답형': 2, '객관식-문장형': 3, '단답형-빈칸': 4, '단답형-문장형': 5, 'OX선택형-O/X': 6, '서술형-코딩': 7}
history = []
def get_completion(prompt, numberKey,count, subject, rags):     
    history.append({'role':'user','content':gpt_prompt.prompt_lst[numberKey](count,subject, rags)}) 
    query = openai.ChatCompletion.create( 
       model="gpt-4-turbo",
       messages=[{"role": "system", "content": gpt_prompt.System_lst[numberKey]}, {'role':'user','content':gpt_prompt.prompt_lst[numberKey](count,subject, rags)}], 
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
    
def query_view(request,numberKey, count, subject, rags): 
    prompt = request.data.get('username') 
    prompt=str(prompt)
    response = get_completion(prompt, numberKey,count, subject, rags)
    return JsonResponse({'response': response}), response 

def get_completion_feedback(prompt):     
    query = openai.ChatCompletion.create( 
       model="gpt-4-turbo",
       messages=[{"role": "system", "content": gpt_prompt.sys_feedback}, {'role':'user','content': prompt}], 
       max_tokens=1024, 
       n=1,
       stop=None,
       temperature=0.5, 
    ) 
    response = query.choices[0].message["content"]
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
        elif i[0:2] == '정답' or i[0:2] == '정닱':
            tempt['answer'] = i[4::]
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
        elif len(i) > 0 and i[0]!= '-' and i[0] != ' ' and i[0:2] != '정답' and i[0:2] != '정닱'  and 1 <= int(i[0]) <= 4:
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
    print(request.data.get('selections'))
    
    ans = {}
    ans['questions'] = []
    problem_lst = []
    coursename = request.data.get('course_name') # course name 가져오기
    # lectureid = request.data.get('lecture_id') # course name 가져오기
    keyword = request.data.get('selectedKeywords') # course name 가져오기
    print(keyword)
    print(keyword[0])
    print(coursename)
    crawl_idx = Sub_dict[coursename]
    print(crawl_idx)
    print(crawl_lst)
    rags = ''
    for i in keyword:
        rags += crawl_lst[crawl_idx](i)
    print(rags)
    print(len(rags))
    professor_user_name = request.user.username # professor username 가져오기
    professor_user_id = request.user.id # professor username 가져오기
    for _ in range(10):
        problem_lst.append('')
    cnt = 0
    for m in range(1,8):
        for tempt in request.data.get('selections'):    
            if 1 <= Quest_dict[tempt] <= 3 and m == Quest_dict[tempt]:
                tmp = dict()
                tmp['type'] = Quest_dict[tempt]
                a, t = query_view(request,Quest_dict[tempt], request.data.get('selections')[tempt], coursename, rags)
                tmp['items'] = GenerateMultipleProblem(t)
                tmp['count'] = request.data.get('selections')[tempt]
                c = request.data.get('selections')[tempt]
                ans['questions'].append(tmp)
                for k in tmp['items']:
                    tempt_content = f'{Quest_dict[tempt]}'
                    for i in k:
                        if i == 'content':
                            tempt_content += '$$'+k[i]
                        elif i == 'options':
                            for id, j in enumerate(k[i]):
                                tempt_content += '$$'+f'{id+1}번 : ' +j
                        elif i == 'answer':
                            tempt_content += '$$'+k[i]
                    tempt_content += f'$${c}'
                    problem_lst[cnt] = tempt_content
                    cnt += 1
            elif 4 <= Quest_dict[tempt] <= 6 and m == Quest_dict[tempt]:
                tmp = dict()
                tmp['type'] = Quest_dict[tempt]
                a, t = query_view(request,Quest_dict[tempt], request.data.get('selections')[tempt], coursename, rags)
                tmp['items'] = GenerateWriteProblem(t)
                tmp['count'] = request.data.get('selections')[tempt]
                c = request.data.get('selections')[tempt]
                ans['questions'].append(tmp)
                for k in tmp['items']:
                    tempt_content = f'{Quest_dict[tempt]}'
                    for i in k:
                        if i == 'content':
                            tempt_content += '$$'+k[i]
                        elif i == 'answer':
                            tempt_content += '$$'+k[i]
                    tempt_content +=  f'$${c}'
                    problem_lst[cnt] = tempt_content
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
def feedback(request): # for professor
    lecture__id = request.data.get('lecture_id')
    
    pl = problem.objects.filter(lecture_id = lecture__id).first()
    
    full_query = ''
    
    problem_lst = [pl.problem_1,pl.problem_2,pl.problem_3,pl.problem_4,pl.problem_5,pl.problem_6,pl.problem_7,pl.problem_8,pl.problem_9,pl.problem_10]
    while problem_lst[len(problem_lst)-1]:
        problem_lst.pop()
    for idx, pro in enumerate(problem_lst):
        lst = list(pro.split("$$"))
        if int(lst[0]) == 1 or int(lst[0]) == 2 or int(lst[0]) == 3:
            full_query += f'{idx+1} 번 문제\n{lst[1]} \n {lst[2]} \n {lst[3]} \n {lst[4]} \n {lst[5]} \n 정답 : {lst[6]}'
        elif int(lst[0]) == 4 or int(lst[0]) == 5 or int(lst[0]) == 6:
            full_query += f'{idx+1} 번 문제\n{lst[1]} \n 정답 : {lst[2]}'    
    obj = answer.objects.filter(lecture_id = lecture__id)
    

    for tempt in obj:
        print(tempt)
        answer_lst = [obj.answer_1,obj.answer_2,obj.answer_3,obj.answer_4,obj.answer_5,obj.answer_6,obj.answer_7,obj.answer_8,obj.answer_9,obj.answer_10]
        while answer_lst[len(answer_lst)-1] == '':
            answer_lst.pop()
        tmp = '\n\n'
        for idx,ans in enumerate(answer_lst):
            tmp += f'{idx+1} 번 답 : {ans} \n'
        tmp += '\n\n'
        full_query += tmp
    t, answer_1 = query_view_feedback(request, full_query)        
    return Response({'message': answer_1}, status = 200)              


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
            rtr['lecture'].append({'name':k.course_name, 'key':k.course_id})
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
        tempt['professor'] = tmp.name
        tempt['lecture_id'] = i.lecture_id
        tempt['check'] = check
        rtr['lecture'].append(tempt)
    print(rtr)
    return Response(rtr, status = 200)
    # return Response({'message':'fail'}, status = 444)/
    
    






