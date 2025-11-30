"""
URL configuration for my_tech_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

import blog_user.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', blog_user.views.AuthTokenObtainPairView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # blog_post
    path('api/posts/', include('blog_post.urls'), name='blog_post'),

    # blog_user
    path('api/user/', include('blog_user.urls'), name='blog_user'),

    # anonymous users
    path('api/anonymous/', include('anonymous_users.urls'), name='anonymous_users'),

    # comment
    path('api/comment/', include('blog_comment.urls'), name='blog_comment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
