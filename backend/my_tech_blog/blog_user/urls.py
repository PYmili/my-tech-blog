from django.urls import path

from blog_user import views

urlpatterns = [
    path('upload-avatar/', views.UploadUserAvatarView.as_view(), name='upload_avatar'),
    path('information/get/', views.UserInformationView.as_view(), name='get_information'),
    path('information/update/', views.UpdateUserInformationView.as_view(), name='update_information'),
    path('password/update/', views.ChangePasswordView.as_view(), name='change_password'),
]