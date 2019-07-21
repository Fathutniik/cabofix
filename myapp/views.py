import random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from myapp.models import Claim


# Create your views here.

def problems(request):
    # получаем все закончиенные тексты
    return render(request, 'problems.html', {'spisok': Claim.objects.all()})


def write(request):
    if request.method == 'GET':

        # TODO: стоит добавить возможность добавить возможность написать с нуля, даже если тексты уже есть
        return render(request, 'index.html')

    if request.method == 'POST':
        poem = Claim()
        poem.text = ""
        poem.text = request.POST['text']
        poem.Imya = request.POST['Imya']
        poem.author = request.user
        if poem.text == '' or poem.Imya == '':
            return redirect('/')
        else:
            # сохраняем
            poem.save()
            return redirect('/problems')




def me(request):
    if request.method == 'GET':
        records = Claim.objects.filter(author=request.user)
        return render(request, 'me.html', {'history': records})



def like(request):
    id = request.GET['id']
    problem = Claim.objects.get(pk=id)
    problem.likes.add(request.user)
    return redirect('/problems')


def index(request):
    # если мы залогинены
    if request.user.is_authenticated:
        return redirect(write)

    else:
        return redirect('/login')


def login_page(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')

        if username == '' or password == '':
            return HttpResponse("Заполните все поля")

        # проверяем правильность логина и пароля
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse("Логин или пароль неверен")


def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')

        if username == '' or password == '' or email == '':
            return HttpResponse("Заполните все поля")

        if User.objects.filter(username=username).exists():
            return HttpResponse("Логин занят")

        # создаем пользователя
        user = User.objects.create_user(username, email, password)
        user.save()

        # "входим" пользователя
        login(request, user)

        return redirect('/')


def logout_page(request):
    logout(request)
    return redirect('/login')
