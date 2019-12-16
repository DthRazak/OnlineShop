from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.shortcuts import render, redirect

from categories.models import Category
from goods.models import Good
from profiles.forms import SignUpForm, LoginForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.username = form.cleaned_data.get('email').split('@')[0]
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.subscribe = form.cleaned_data.get('subscribe')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            auth_login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    goods = Good.objects.filter(featured=True)[:3]
    categories = Category.objects.all()[::1]
    return render(request, 'signup.html', {'form': form, 'goods': goods, 'categories': categories})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email').split('@')[0]
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                auth_login(request, user)
                return redirect('/')
    else:
        form = LoginForm()
    goods = Good.objects.filter(featured=True)[:3]
    categories = Category.objects.all()[::1]
    return render(request, 'login.html', {'form': form, 'goods': goods, 'categories': categories})


def logout(request):
    auth_logout(request)
    return redirect('/profile/login')
