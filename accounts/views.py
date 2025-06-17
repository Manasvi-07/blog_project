from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import RegisterForm, EmailLoginForm

class RegisterView(CreateView):
    def get(self, request):
        return render(request, 'registration/register.html', {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:home')  
        return render(request, 'registration/register.html', {'form': form})


class EmailLoginView(LoginView):
    def get(self, request):
        form = EmailLoginForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('blog:home')
        return render(request, 'registration/login.html', {'form': form})

class EmailLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')

