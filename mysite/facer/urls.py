from django.urls import path

from . import views

app_name = 'facer'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/face', views.face, name='face'),
]