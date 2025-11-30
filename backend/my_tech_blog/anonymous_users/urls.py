from django.urls import path

from anonymous_users import views


urlpatterns = [
    path('register/', views.RegisterAnonymousView.as_view(), name='anonymous_register'),
    path('get/',views.GetAnonymousUserView.as_view(), name='get_anonymous_user'),
]