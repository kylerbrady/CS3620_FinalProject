from django.urls import path
from . import views

app_name = 'hangman'
urlpatterns = [
    path('', views.index, name="index"),
    path('gamePage/', views.hangman, name="gamePage"),
    path('displayScore/', views.displayScore, name="displayScore"),

]
