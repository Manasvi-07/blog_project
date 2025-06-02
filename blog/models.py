from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    image = models.ImageField(upload_to = 'post_images/', blank=True, null=True)
    Category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True, blank = True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.Post.title}'

