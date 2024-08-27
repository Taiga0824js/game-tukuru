from django.shortcuts import render

def game(request):
    return render(request, 'game_otamesi/index.html')