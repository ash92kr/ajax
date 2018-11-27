from django.shortcuts import render, get_object_or_404, resolve_url, redirect
from django.views.generic import ListView, CreateView,DetailView
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse

# Create your views here.

class PostList(ListView):
    model = Post
    
class PostCreate(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content',]

class PostDetail(DetailView):
    model = Post
    
    def get_object(self):
        post = Post.objects.prefetch_related('comment_set__user').select_related('user')
        return get_object_or_404(post, pk=self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
        
class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content',]
    
    def form_valid(self,form):
        post = Post.objects.get(id = self.kwargs.get('pk'))
        self.object = form.save(commit=False)
        self.object.post = post
        self.object.user = self.request.user
        self.object.save()
        
        return super().form_valid(form)

# 로그인을 해야 like 버튼을 누를 수 있다        
@login_required
def like(request, pk):
    if request.is_ajax():  # ajax를 통해 요청이 들어올 경우 
        user = request.user
        post = Post.objects.get(pk=pk)  # 오른쪽의 pk가 위의 pk를 받음
        # 사용자가 like를 눌렀으면 취소
        if post.like.filter(id=user.id).exists():  # 사용자가 좋아요 버튼을 이미 눌렀다면 True, 없으면 False를 나타냄
            post.like.remove(user)  # 사용자의 정보를 지움
            
        # 사용자가 안눌렀으면 좋아요를 나타냄
        else :
            post.like.add(user)
        data = {'likes_count' : post.like.count()}  # 좋아요를 누른 사람의 수를 알려줌
        return HttpResponse(json.dumps(data), content_type="application/json")  # 딕셔너리를 json 형태로 만듦
        
    else : # ajax를 통해 사용자의 요청이 들어오지 않은 경우
        return redirect(resolve_url('posts:detail', pk))   # 해당 포스트를 다시 보도록 설정