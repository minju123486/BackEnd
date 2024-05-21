from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import openai
import os
import environ
import pyperclip
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
# from tkinter import Tk, messagebox


user_data = dict()

from pathlib import Path
from django.shortcuts import render 
from django.http import JsonResponse
from myapp import gpt_prompt
from openai import OpenAI
import os
from community.models import post
from .models import daily_model, daily_class
env = environ.Env()
environ.Env.read_env(Path(__file__).resolve().parent/'.env')
# openai.api_key = env('Key')
# 인삿말
client = OpenAI(
    # This is the default and can be omitted
    api_key=env('Key')
)
def hello(where, tmi):
    model_engine = "gpt-3.5-turbo" # 장소 fine-tuning 3.5 turbo model  ft:gpt-3.5-turbo-0125:personal::9JO9ePp4
    prompt = prompt_hello.format(
        where, tmi, where, tmi, where, tmi, where, tmi # format 요소 넣기
    )
    
    try:
        response = client.chat.completions.create(
            model=model_engine,
            messages=[
                {"role": "system", "content": "당신은 공부 일기 블로그 포스팅의 인삿말을 생성하는 20대 대학생입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1028
        )
        print('===============')
        print(response)
        print('===============')
        text = response.choices[0].message.content
        print(text)
        return text
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

prompt_hello = '''
내가 제공하는 예시 문장들 중에 하나를 출력해

### 예시 문장 
- "안니옹하세용~~ 다들 좋은 하루 보내셨나요?! 오늘은 {}에서 공부 일기나 써보려구요!! 아 맞다 저 오늘 {},,, 여튼 일기 시작해볼게요~" 
- "안녕하세요! {}에서 일기 작성하기 프로젝트~ 원래 더 일찍 쓰려고 했는데 너무 피곤해서 이제야 쓰네요 ㅎㅎ;;; 아 근데 저 오늘 {},, 여튼 일기 써볼게요~"
- "{}는 다 좋은데 맨날 오니까 질리네요 질려... 그냥 집갈까 하다가 공부 일기만 후딱 쓰고 가겠습니다. 아니 근데 저 오늘 {},, 진짜 열 받네요;;;; 일기로 달래보겠습니다!!!!"
- "안녕하세요~~ {}에서 공부하는 사람들이 진짜 많네요?? 저는 커피나 마시면서 공부 일기쓰러 왔는데,, 아 그리고 저 오늘 {},, 쩝 암튼 일기 써볼게욥"
'''


# 일기
def generate_blog(greeting, tmi, who, what, why, where, when, how, prompt_korean_template):
    model_engine = "gpt-4-turbo"  # 속도 = 3.5 turbo, 성능 = 4 turbo
    prompt_korean = prompt_korean_template.format(
        who, what, why, where, when, how, what, what, what, what, what, what, what
    )
    
    try:
        response = client.chat.completions.create(
            model=model_engine,
            messages=[
                {"role": "system", "content": "공부 일기 블로그 포스팅을 생성하는 AI 시스템입니다."},
                {"role": "user", "content": prompt_korean}
            ],
            max_tokens=4096,
            temperature=0.8
        )
        text = response.choices[0].message.content
        pyperclip.copy(text)  # 클립보드에 텍스트 복사
        return text
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

prompt_korean_template = '''
아웃라인 구성 : 제목 - 인사 - 본문(섹션1~7) - 맺음말로 구성해.

블로그 포스트를 마크다운 형식으로 작성해. 중요한 단어나 문장을 굵게, 기울임꼴 또는 밑줄로 강조해.
제목은 블로그 게시물에 대한 눈에 띄고 SEO 친화적인 제목을 생성해.
제목은 무조건 '제목:' 을 앞에 기재하세요.
인사는 항상 "안니옹하세용. 한량 규 입니다. 요즘 제가 정신이 하나도 없는데요! 이 일기 생성이 너~~~무 안되서 머리가 터질 것 같아요! 그래도 다시 한 번 힘내보겠습니다!" 로 출력해.

다음 줄에는 {{tmi}}에 대해서 언급을 해주고, "오늘은 {{what}}에 대해서 공부해봤습니다~ 이게 뭔지 이제 설명해드릴게요!" 출력해

일기 형식으로 작성하고 말투는 친근한 말투를 사용하며, 상세한 설명을 해주는 것이 특징이야.

자주 쓰는 표현은 "~했다.", "~였는데, ~다." 

표현의 예시 1 : "오늘은 what에 대한 공부를 했다. 사실 what에 대해서 관심을 가지고 있었는데, 시간이 없어서 하지 못했다."
표현의 예시 2 : "어제는 PostgreSQL에 대한 공부를 했는데, 무슨 말인지 못 알아먹겠다."
표현의 예시 3 : "앞으로 공부를 열심히 하겠다고 다짐했다!! 지금까지는 대충했었는데, 앞으론 진짜 빡공간다!!"

작성자는 "{}"야.
"{}"에 대한 공부를 했고, 공부를 한 이유는 "{}", "{}"에서 "{}" 공부를 했어, "{}" 방식으로 공부를 했어. 이것에 대한 공부 일기를 작성해.

### 섹션 1: 
"{}"에 대한 기본 이해
(섹션 1에서는 {{what}}이 무엇인지 정의하고, 기본적인 개념을 설명해. 그 다음 이 기술이 왜 중요한지 설명해.)

### 섹션 2:
"{}"와 역사와 발전 과정
(섹션 2에서는 {{what}} 기술 or 프로그래밍이 어떻게 시작되었는지에 대한 역사적 배경을 설명해. 그 다음 중요한 마일스톤과 최근 혁신적 발전들을 강조해.)

### 섹션 3: 
"{}"에 대한 원리와 구조
({{what}}을 구성하는 기본적인 알고리즘과 원리에 대해 설명해. 그 다음 이러한 원리가 실제로 어떻게 작동하는지 예를 들어 설명해.)

### 섹션 4: 
"{}"을 활용한 사례
(실제 {{what}} 기술 or 프로그래밍이 적용된 다양한 사례들을 소개해. 그 다음 각 사례에서 {{what}}이 어떻게 문제를 해결했는지 설명해.)

### 섹션 5: 
"{}"을 활용할만한 창의적 아이디어
({{what}} 기술을 사용하여 해결할 수 있는 새로운 문제나 창의적 프로젝트 아이디어를 제시해.)

### 섹션 6: 
"{}"에 대한 꿀팁
({{what}} 공부를 시작하는 데 도움이 될 수 있는 팁과 리소스를 하이퍼링크 형태로 제공해. 그 다음 공부를 하는 동안 추천하는 학습 방법을 공유해.)

### 섹션 7: 
"{}"을 주제로 한 질의응답
(3개 이상의 질문과 답변으로 구성해)

글의 끝에 각 섹션에서 논의한 주제에 대한 해시태그와 함께 내 생각을 맺음말로 정리해. 이렇게 각 섹션을 명확하게 구분하고 각각의 주제에 대해 상세하게 풀어나가는 구조를 사용해. 짧지 않게 상세히 퀄리티 높게 작성해.

맺음말에 대한 예시 말투를 참고해
ex 1) 오늘 NLP에서 중요하다고 생각하는 문장 토큰화에 대해 공부했다. 근데 생각보다 익숙한 내용이어서 엥 뭐지? 싶었는데, 알고보니까 단어 토큰화랑 매커니즘 자체는 동일하더라
그래서 오늘 공부는 조금 수월하게 했다. 다음 단원은 테이블 벡터에 대해서 공부하는데, 벡터에 대해서 잘 모르는 것 같아서 조금 걱정이다.

ex2) 평소에 딥러닝에 대해서 공부하면 머리가 뒤지게 아팠는데, 오늘은 왜케 잘 풀리는지 모르겠다. 그래서 오늘 평소보다 집중도 잘하고 좋았다. 내일도 평화롭게 공부하고싶다.. 에휴.. 파이팅 사울~

상세하고 정확한 정보를 제공해.
짧게쓰면 벌을 줄 거야.
정말 중요한 일기야, 잘 하면 30달러를 팁으로 줄게.
--- 를 활용해서 파트를 나눠서 작성해.

제목이랑 본문에 어울리는 이모지를 같이 작성해주고, 느낌표와 같이 강조할 수 있는 부분은 친근한 표현과 함꼐 강조해

답변할 때는 오직 검증된 출처에서 가져온 정보만을 사용해.

할루시네이션이 있으면 절대 안돼. 정말 중요한 문서야.
'''
# 사용자 입력 받기
# where = input("어디서? Ex) 공대: ")
# tmi = input("오늘의 tmi를 작성해주세요: ")

# 첫 번째 코드 실행하여 인삿말 생성
# greeting = hello(where, tmi)

# if greeting:
#     who = input("누구신가요?")
#     what = input("무엇을 공부하셨나요?")
#     why = input("왜 그것을 공부하셨나요?")
#     when = input("언제 공부하셨나요?")
#     how = input("어떤식으로 공부했나요?")

#     blog_content = generate_blog(greeting, tmi, who, what, why, where, when, how, prompt_korean_template)
#     if blog_content:
#         final_blog_content = f"{greeting}\n\n{blog_content}"
#         print(final_blog_content)
#         pyperclip.copy(final_blog_content) 

#         # root = Tk()
#         # root.withdraw()
#         # messagebox.showinfo("알림띠~", "생성한 공부 일기가 복사되었습니다!")
#         # root.destroy() 
#     else:
#         print("블로그 생성에 실패했습니다.")
# else:
#     print("인삿말 생성에 실패했습니다.")
    
@api_view(['POST'])  
def generate_daily(request):
    who = request.data.get('who')
    when = request.data.get('when')
    where = request.data.get('where')
    what = request.data.get('what')
    how = request.data.get('how')
    why = request.data.get('why')
    tmi = request.data.get('others')
    print("WWOWWOW")
    now = datetime.now()


    n_year = now.year
    n_month = now.month
    n_day = now.day
    
    greeting = hello(where, tmi)
    print(greeting)
    blog_content = generate_blog(greeting, tmi, who, what, why, where, when, how, prompt_korean_template)
    title = f'{n_year}.{n_month}.{n_day}. '
    if blog_content:
        final_blog_content = f"{greeting}\n\n{blog_content}"
        lst = list(final_blog_content.split("\n"))
        print(lst)
        no_title_lst = []
        check = 1
        for k in lst:
            if '제목' in k and check == 1:
                title += k
                check = 0
            else:
                no_title_lst.append(k)
        print("------------------")
        print(title)
        print("------------------")
        # pyperclip.copy(final_blog_content)
        return Response({'diaryText' : no_title_lst, 'title' : title}, status=status.HTTP_200_OK) 
    
    
    
    
    
    
    
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def daily_save(request):
    title = request.data.get('title')
    print('-----------')
    print(title)
    print('-----------')
    content = request.data.get('content')
    ch = int(request.data.get('check'))
    username = request.user.username
    now = datetime.now()


    n_year = now.year
    n_month = now.month
    n_day = now.day
    n_hour = now.hour
    n_minute = now.minute
    obj = daily_model(author = username, title = title, content = content, year = n_year, month = n_month, day = n_day, hour = n_hour, minute = n_minute)
    obj.save()
    if ch == 1:
        tmp = post(author = username, title = title, content = content, year = n_year, month = n_month, day = n_day, hour = n_hour, minute = n_minute, watch = 0, like = 0, comment_number = 0)
        tmp.save()
    return Response({'message' : 'success'}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def daily_view(request):
    return Response({'title':['2024.05.12', '2024.05.31', '2024.05.14' ],'id':[1, 2, 3 ]}, status = 200)               
    

@api_view(['GET'])
def mock_diary(request):
    user_name = request.user.username
    tempt = daily_model.objects.filter(author = user_name)
    title = []
    id = []
    content = []
    tmp = {}
    for i in tempt:
        title.append(i.title)
        id.append(i.id)
        content.append(i.content[:50]+'....')
    tmp['title'] = title
    tmp['content'] = content
    tmp['id'] = id
    
    
    return Response(tmp, status = 200)             


@api_view(['GET'])
def daily_view(request):
    user_name = request.user.username
    tempt = daily_model.objects.filter(author = user_name)
    title = []
    id = []
    content = []
    tmp = {}
    for i in tempt:
        title.append(i.title)
        id.append(i.id)
    tmp['title'] = title
    tmp['id'] = id
    return Response(tmp, status = 200) 
  
    
@api_view(['POST'])
def daily_look(request):
    id = request.data.get('id')
    tempt = daily_model.objects.filter(id = id).first()
    return Response({'title':tempt.title, 'content':tempt.content}, status = 200) 




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def classdaily_save(request):
    title = request.data.get('title')
    print('-----------')
    print(title)
    print('-----------')
    content = request.data.get('content')
    print('--------------------')
    print(content)
    print('======================')
    username = request.user.username
    now = datetime.now()


    n_year = now.year
    n_month = now.month
    n_day = now.day
    n_hour = now.hour
    n_minute = now.minute
    obj = daily_class(author = username, title = title, content = content, year = n_year, month = n_month, day = n_day, hour = n_hour, minute = n_minute)
    obj.save()
    return Response({'message' : 'success'}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def classdaily_view(request):
    user_name = request.user.username
    tempt = daily_class.objects.filter(author = user_name)
    title = []
    id = []
    tmp = {}
    for i in tempt:
        title.append(i.title)
        id.append(i.id)
    tmp['title'] = title
    tmp['id'] = id
    return Response(tmp, status = 200)    


@api_view(['POST'])
def classdaily_look(request):
    id = request.data.get('id')
    tempt = daily_class.objects.filter(id = id).first()
    return Response({'title':tempt.title, 'content':tempt.content}, status = 200) 


    

    
    
prompt_study_diary = '''
오늘 수업에서 무엇을 배웠는지 수업일기를 작성하는 20대 대학생입니다.

제목을 생성합니다. 제목은 무조건 '제목:' 을 앞에 기재하세요.

입력으로 받은 내용을 바탕으로 학습 일기를 작성하세요.
주어진 주제에 대해 이해가 잘 되는 부분과 안 되는 부분을 나눠서 작성하세요.

학생에게 {}에 대해 피드백을 주는 느낌으로 작성하세요.

본문에 어울리는 이모지를 같이 작성하고, 느낌표와 같이 강조할 수 있는 부분은 친근한 표현과 함께 강조하세요.

입력 예시:
오늘 PostgreSQL을 공부했는데 TABLE 같은 형식은 다 알겠는데 오픈소스 데이터베이스 개념이 조금 생소하더라

출력 예시:
오늘은 PostgreSQL을 공부했는데 TABLE 같은 형식은 다 이해를 한 것 같다. 하지만 오픈소스 데이터베이스라는 개념이 조금 헷갈리는데 찾아보니 오픈소스 데이터베이스라는 것은 (오픈소스 데이터베이스 개념 설명, 동작 원리) 이런 것이었다. 앞으로도 오픈소스 데이터베이스에 대해서 더 열심히 공부해야겠다! 😊
'''
    
    
    
    
@api_view(['POST'])   
def study_diary(request):
    global prompt_study_diary
    what = request.data.get('what')
    model_engine = "gpt-3.5-turbo"  # 장소 fine-tuning 3.5 turbo model  ft:gpt-3.5-turbo-0125:personal::9JO9ePp4
    today_date = datetime.today().strftime('%Y-%m-%d')
    prompt = prompt_study_diary.format(what, today_date)
    now = datetime.now()


    n_year = now.year
    n_month = now.month
    n_day = now.day
    n_hour = now.hour
    n_minute = now.minute
    try:
        response = client.chat.completions.create(
            model=model_engine,
            messages=[
                {"role": "system", "content": "당신은 공부 일기 블로그 포스팅의 인삿말을 생성하는 20대 대학생입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1028
        )
        text = response.choices[0].message.content
        tmp = list(text.split('\n'))
        title = f'{n_year}.{n_month}.{n_day}.'
        for k in tmp:
            if '제목' in k:
                title += k
        return Response({'title':title, 'content':text}, status = 200)
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({'title':'wow', 'content':'dd'}, status = 200)



# 예시 실행