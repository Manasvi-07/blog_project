from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import RegisterForm, PostForm
from .models import Post
from django.views.generic.list import ListView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView, FormMixin
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django import forms


def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)  
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm() 
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = EmailLoginForm()
    return render(request, 'registration/login.html',{'form':form})

class EmailLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid email or password")

        user = authenticate(username=user.username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid email or password")

        self.user = user
        return cleaned_data

    def get_user(self):
        return self.user
    

class LogoutView(LogoutView):
    next_page = reverse_lazy('login')
    template_name = 'logout.html'
    allow_get = True

class PostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-created']



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/edit_post.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser
    


    