from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import PostList, PostCreateView, PostUpdateView, PostDeleteView, PostDetailView, HomeView

app_name = 'blog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/create/', PostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/edit/<int:pk>/', PostUpdateView.as_view(), name='edit_post'),
    path('posts/delete/<int:pk>/', PostDeleteView.as_view(), name='delete_post'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    