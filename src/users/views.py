from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, LoginForm
from django.urls import reverse
from .models import CustomUser
# Create your views here.

def register_view(request: HttpRequest):
    if request.method == "GET":
        return render(request, "register.html", {"form": CustomUserCreationForm})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(form.data.get("email"))
            user.set_password(form.data.get("password1"))
            user.save()
            return redirect("/login/")
        if not form.is_valid():
            return render(request, "register.html", {"form": CustomUserCreationForm,
                                                     "errors": form.errors})

def login_view(request: HttpRequest):
    if request.method == "GET":
        return render(request, 'login.html', {'form': LoginForm})
    elif request.method == "POST":
        data = {"username": request.POST.get("username"), "password": request.POST.get("password")}
        form = LoginForm(data=data)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('/')
            elif not user:
                return HttpResponse('<h1>No user</h1>')
        elif not form.is_valid():
            return render(request, "login.html", {"content": "Неверный Email или пароль.",
                                                  "form": LoginForm, "errors": form.errors})

@login_required
def logout_view(request: HttpRequest):
    if request.method == "GET":
        logout(request)
        return redirect(reverse(login_view))


