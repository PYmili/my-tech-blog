from django.urls import path

from blog_comment import views

urlpatterns = [
    path('list/', views.CommentListView.as_view(), name='comment_list'),
    path('add/', views.CommentPostView.as_view(), name='comment_post'),
]