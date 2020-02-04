# from django.contrib import admin
from django.urls import path, include
# from . import views
from Insta.views import addComment, addLike, HelloDjango, PostsView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserDetailView, ExploreView, UserUpdateView, toggleFollow
urlpatterns = [
    path('helloworld', HelloDjango.as_view(), name = 'helloworld'),
    path('', PostsView.as_view(), name = 'posts'),
    path('explore', ExploreView.as_view(), name = 'explore'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post_detail'),
    path('posts/new/', PostCreateView.as_view(), name = 'make_post'),
    path('posts/update/<int:pk>/', PostUpdateView.as_view(), name = 'post_update'),
    path('posts/delete/<int:pk>/', PostDeleteView.as_view(), name = 'post_delete'),
    path('like', addLike, name='addLike'),
    path('togglefollow', toggleFollow, name='toggleFollow'),
    path('comment', addComment, name = 'addComment'),
    path('user/<int:pk>/', UserDetailView.as_view(), name = 'user_detail'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name = 'user_update'),
]
