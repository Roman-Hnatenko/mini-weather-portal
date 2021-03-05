from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("reset/", views.reset_weather, name='reset_weather'),
    path("show/", views.HistoryPage.as_view()),
    path('filter/', views.FilterCity.as_view(), name='filter'),
    path('', views.GetPageView.as_view()),

]
