from .views import PostCreateView, PostDetailView, PostListView, PostLikeView
from django.urls import path

app_name = 'posts'

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='new-post'),
    path('', PostListView.as_view(), name='list'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('like/<int:post_id>/', PostLikeView.as_view(), name='like'),
]
