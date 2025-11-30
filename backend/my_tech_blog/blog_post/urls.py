from django.urls import path
from blog_post import views

urlpatterns = [
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
    path('recent/', views.RecentView.as_view(), name='recent'),
    path('list/', views.PostListView.as_view(), name='list'),
    path('hot/', views.PostHotListView.as_view(), name='hot'),
    path('detail/', views.PostDetailView.as_view(), name='detail'),
    path('add/', views.PostAddView.as_view(), name='category-add'),
    path('delete/', views.PostDeleteView.as_view(), name='category-delete'),
    path('update/', views.PostUpdateView.as_view(), name='category-update'),
    path('category/list/', views.CategoryListView.as_view(), name='category-list'),
    path('category/add/', views.CategoryAddView.as_view(), name='category-add'),
    path('category/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    path('like/', views.LikePostView.as_view(), name='like'),
    path('traffic-statistics/', views.TrafficStatisticsPostView.as_view(), name='traffic-statistics'),
    path('chart-data/', views.PostChartDataView.as_view(), name='chart-data'),
]