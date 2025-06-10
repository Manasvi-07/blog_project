from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import PostList, PostCreateView, PostUpdateView, PostDeleteView, LogoutView, PostDetailView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/create/', PostCreateView.as_view(), name='create_post'),
    path('posts/edit/<int:pk>/', PostUpdateView.as_view(), name='edit_post'),
    path('posts/delete/<int:pk>/', PostDeleteView.as_view(), name='delete_post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)