from django.contrib import admin
from django.urls import path
from .views import RegisterView, Loginview, userview, logoutview

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', Loginview.as_view()),
    path('user', userview.as_view()),
    path('logout', logoutview.as_view()),
]