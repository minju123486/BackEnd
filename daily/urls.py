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
from daily import views

urlpatterns = [
    path('generate_daily/', views.generate_daily),
    path('daily_save/', views.daily_save),
    path('mock_diary/', views.mock_diary),
    path('daily_view/', views.daily_view),
    path('daily_look/', views.daily_look),
    path('classdaily_save/', views.classdaily_save),
    path('classdaily_view/', views.classdaily_view),
    path('classdaily_look/', views.classdaily_look),
    path('study_diary/', views.study_diary)
]
