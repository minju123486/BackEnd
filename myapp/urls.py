"""capde URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('', views.index),
    path('GenerateQuestion/', views.GenerateQuestion),
    path('course_view/', views.course_view),
    path('lecture_generate/', views.lecture_generate),
    path('lecture_show/', views.lecture_show),
    path('lecture_view/', views.lecture_view),
    path('lecture_apply/', views.lecture_apply),
    path('my_lecture_show/', views.my_lecture_show)
]
