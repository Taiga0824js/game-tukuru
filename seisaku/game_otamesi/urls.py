from django.urls import path
from . import views

app_name = "game_otamesi"

urlpatterns = [
    path('index/', views.game, name='index'),
]