from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


user_data = dict()


def index(request):
    return HttpResponse("Communication start")

@api_view(['POST'])
def login_view(request):
    global user_data
    username = request.data.get('username')
    password = request.data.get('password')
    check = True
    print(username)
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