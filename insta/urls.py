from django.urls import path
from . import views

app_name = 'insta'

urlpatterns = [
    path('', views.index, name='index'),
    path('wordcloud/', views.wordcloud, name='wordcloud'),
    path('map/', views.map, name='map'),
]
