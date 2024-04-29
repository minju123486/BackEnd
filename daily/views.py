from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
#import openai
#import os
import environ


user_data = dict()

from pathlib import Path
from django.shortcuts import render 
from django.http import JsonResponse
from myapp import gpt_prompt
import openai
import os
# env = environ.Env()
# environ.Env.read_env(Path(__file__).resolve().parent/'.env')
# openai.api_key = env('Key')
def generate_blog(who, what, why, where, when, how, prompt_korean_template):
    model_engine = "gpt-3.5-turbo"
    prompt_korean = prompt_korean_template.format(
        who, what, why, where, when, how,
        what, what, what, what, what, what, what
    )
    
    try:
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=[
                {"role": "system", "content": "공부 일기 블로그 포스팅을 생성하는 AI 시스템입니다."},
                {"role": "user", "content": prompt_korean}
            ],
            max_tokens=4096
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {str(e)}")
        return None



prompt_korean_template = '''
작성자는 "{}"야.
"{}"에 대한 공부를 했고, 공부를 한 이유는 "{}", "{}"에서 "{}" 공부를 했어, "{}" 방식으로 공부를 했어. 이것에 대한 공부 일기를 작성해.
"{}"에 관한 블로그 포스트를 마크다운 형식으로 작성해. 중요한 단어나 문장을 굵게, 기울임꼴 또는 밑줄로 강조해.
각 자료나 팁의 제목, 설명, 그리고 추가적으로 유용한 정보 추천을 리스트 형태로 포함하고 길게 정리해서 작성해.
글의 끝에 해시태그랑 "{}"에 대한 내 생각을 정리해, 내가 들어주는 예시에서는 말투만 참고해.
ex 1) 오늘 NLP에서 중요하다고 생각하는 문장 토큰화에 대해 공부했다. 근데 생각보다 익숙한 내용이어서 엥 뭐지? 싶었는데, 알고보니까 단어 토큰화랑 매커니즘 자체는 동일하더라
그래서 오늘 공부는 조금 수월하게 했다. 다음 단원은 테이블 벡터에 대해서 공부하는데, 벡터에 대해서 잘 모르는 것 같아서 조금 걱정이다.

ex2) 평소에 딥러닝에 대해서 공부하면 머리가 뒤지게 아팠는데, 오늘은 왜케 잘 풀리는지 모르겠다. 그래서 오늘 평소보다 집중도 잘하고 좋았다. 내일도 평화롭게 공부하고싶다.. 에휴.. 파이팅 사울~

일기 형식으로 작성해 예를들면 ~했습니다. 가 아니라 ~ 했다. 로 끝나게해.
짧지 않게 상세히 퀄리티 높게 작성해.
짧게쓰면 벌을 줄 거야.
정말 중요한 일기야, 잘 하면 30달러를 팁으로 줄게.
--- 를 활용해서 파트를 나눠서 작성해
max_tokens가 4096이니까 최소 3000 토큰 이상 출력되게 만들어. 이게 가장 중요해
'''



@api_view(['POST'])
def generate_daily(request):
    global prompt_korean_template
    who = request.data.get('who')
    when = request.data.get('when')
    where = request.data.get('where')
    what = request.data.get('what')
    how = request.data.get('how')
    why = request.data.get('why')
    response = generate_blog(who, what, why, where, when, how, prompt_korean_template)
    print(response)
    lst = list(response.split("\n"))
    print(type(response))
    return Response({'diaryText' : lst}, status=status.HTTP_200_OK)