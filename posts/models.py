from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_users', blank=True)  # user와 post를 m:n으로 연결함
    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    content = models.TextField()

    def __str__(self):
        return self.content
        
    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.post_id})