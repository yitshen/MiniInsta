# from django.shortcuts import render
from annoying.decorators import ajax_request
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from Insta.models import Post, Like, Comment, InstaUser, UserConnection
from django.shortcuts import get_object_or_404

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from Insta.forms import CustomUserCreationForm
from django.db.models import Q

class HelloDjango(TemplateView):
    template_name = 'test.html'
# Create your views here.

class PostsView(ListView):
    model = Post
    template_name = 'index.html'

    def get_queryset(self):
        try:
            current_user = self.request.user
            following = set()
            for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
                following.add(conn.following)
            return Post.objects.filter(author__in=following)
        except:
            return Post.objects.filter()

class ExploreView(ListView):
    model = Post
    template_name = 'index.html'
    def get_queryset(self):
        try:
            current_user = self.request.user
            following = set()
            for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
                following.add(conn.following)
            following.add(self.request.user)
            return Post.objects.filter(~Q(author__in=following))
        except:
            return Post.objects.filter()


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class UserDetailView(DetailView):
    model = InstaUser
    template_name = 'user_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # current_user = self.request.user

    template_name = 'post_create.html'
    # initial = {'author', request.user}
    fields = '__all__'
    # fields = ['title','image']
    login_url = 'login'
    # def get_initial(self):
    #     state = get_object_or_404(Post, author=Post.author.id)
    #     return {
    #         'author':state,
    #     }

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']
    login_url = 'login'

class UserUpdateView(UpdateView):
    model = InstaUser
    template_name = 'user_update.html'
    fields = ['email','profile_pic']
    login_url = 'login'


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url  = reverse_lazy("posts")
    login_url = 'login'
    
class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")

@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }

@ajax_request
def addComment(request):
    comment_text = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    commenter_info = {}

    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()
        username = request.user.username
        commenter_info = {
            'username': username,
            'comment_text': comment_text
        }
        result = 1
    except Exception as e:
        print(e)
        result = 0
    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }

@ajax_request
def toggleFollow(request):
    current_user = InstaUser.objects.get(pk=request.user.pk)
    follow_user_pk = request.POST.get('follow_user_pk')
    follow_user = InstaUser.objects.get(pk=follow_user_pk)

    try:
        if current_user != follow_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(creator=current_user, following=follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(creator=current_user, following=follow_user).delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_user_pk': follow_user_pk
    }
