from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status  # HTTP 상태 코드
from rest_framework.response import Response  # DRF 응답 클래스
from rest_framework.views import APIView  # DRF API 뷰 클래스
from django.contrib.auth import authenticate,login,logout  # Django의 인증 함수
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views import View
user_data = dict()
from django.http import HttpRequest
from rest_framework.permissions import AllowAny
from django.shortcuts import render 
from django.http import JsonResponse
from myapp import gpt_prompt
import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from .models import school
def index(request):
    return HttpResponse("Communication start")


def sign_up(request):
    sign_name_id = request.data.get('id')
    sign_password = request.data.get('password')
    print('check password',sign_password)
    sign_name = request.data.get('name')
    sign_student_id = request.data.get('studentid')
    sign_e_mail = request.data.get('email')
    sign_phone_number = request.data.get('phone')
    sign_year = request.data.get('year')
    sign_month = request.data.get('month')
    sign_day = request.data.get('day')
    sign_gender = request.data.get('gender')
    check_usertype = request.data.get('usertype')
    sign_grade = request.data.get('grade')
    instance = school.objects.create_user(username = sign_name_id, password  = sign_password, name = sign_name, studentid  = sign_student_id, email  = sign_e_mail, phone = sign_phone_number, year = sign_year, month = sign_month, day = sign_day, gender = sign_gender, usertype = check_usertype, grade = sign_grade)
    instance.save()
    print(f'{check_usertype} {sign_name_id} 회원가입 하였습니다.')
    return True


@api_view(['POST'])
def id_check(request):
    check_name_id = request.data.get('id')
    try:
        obj = school.objects.get(username = check_name_id)
        print(obj.password)
        print("닉네임 중복확인")
        return Response({'message': 'Fail'}, status=409)
    except:
        print("닉네임 중복아님")
        return Response({'message': 'Success'}, status=201)
    
    
def sign_in(request):
    check_name_id = request.data.get('username')
    check_password = request.data.get('password')
    check_usertype = request.data.get('usertype')
    print(f'{check_usertype} {check_name_id} 로그인 시도하였습니다.', end = '   ')
    try:
        obj = school.objects.get(id = check_name_id)
        if obj.password == check_password:
            print("로그인 성공")
            return True
        else:
            print("로그인 실패")
            return False
    except:
        print("로그인 실패")
        return False
    
    
class CustomTokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        # 요청에서 username과 password를 가져옵니다
        user_name = request.data.get('username')
        user_type = request.data.get('usertype')
        password = request.data.get('password')
        print(f'{user_type} {user_name} 로그인 시도하였습니다.', end = '   ')
        try:
            user = authenticate(request, username=user_name, password=password)
            obj = school.objects.get(username = user_name)
            print(obj.usertype)
            if obj.usertype != user_type:
                print("유저 타입 맞지 않음.")
                return Response({'error': '인증 실패'}, status=status.HTTP_401_UNAUTHORIZED)
            if not user:
                print("최종 로그인 실패")
                return Response({'error': '인증 실패'}, status=status.HTTP_401_UNAUTHORIZED)
            print(password)
            print("사실 여기까지는 옴")
            # 사용자를 위한 새로운 refresh 토큰과 access 토큰을 생성합니다.
            refresh = TokenObtainPairSerializer.get_token(user)
            print("로그인 성공")
            login(request, user)

            return Response({'refresh_token': str(refresh),  # Refresh 토큰
                'access_token': str(refresh.access_token),  # Access 토큰
            }, status=status.HTTP_200_OK)
        except:
            print("except 최종 로그인 실패")
            return Response({'error': '인증 실패'}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutAPIView(APIView):
    def post(self, request):
        try:
            # 사용자 세션 로그아웃
            logout(request)
            return Response(status=200)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)  
    
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        sign_up(request)
        return HttpResponse("User created successfully", status=200) 
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_view(request):
    print(f'토큰 체크 id ======= {request.user.id}')
    return Response(data={"message": "This is a protected GET request."})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_view(request):
    print(f'토큰 체크 id ======= {request.user.id}')
    return Response(data={"message": "This is a protected GET request."})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def name_check(request):
    print(f'이름 체크 id ======= {request.user.name}')
    print(f'이름 체크 id ======= {request.user.name}')
    return Response(data={"name": request.user.name})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def position_check(request):
    if request.user.usertype == 'student':
        return Response(data={"message": "This is a protected GET request."},status=200)
    elif request.user.usertype == 'professor':
        return Response(data={"message": "This is a protected GET request."},status=201)
    else:
        return Response(data={"message": "This is a protected GET request."},status=202)
