from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class BlogUser(AbstractUser):
    # 用户头像
    avatar = models.ImageField(
        # 上传到avatar目录，安装年月日分层
        upload_to='avatar/%Y/%m/%d/',
        null=True,
        blank=True,
        default='avatar/default.jpg',
        verbose_name='头像'
    )

    # 个人简介/签名
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='个人简介'
    )

    # GitHub 链接
    github_home_link = models.URLField(
        max_length=39,
        blank=True,
        verbose_name='GitHub主页地址'
    )

    # 性别
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
        ('prefer_not_to_say', '不愿透露'),
    ]
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True,
        verbose_name='性别'
    )

    # 生日
    birth_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='生日'
    )

    # 居住地/城市
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='所在地'
    )

    # 信息更新时间
    profile_updated_at = models.DateTimeField(auto_now=True, verbose_name='资料更新时间')

    def __str__(self):
        # 可以根据情况返回昵称或用户名
        return self.nickname if self.nickname else self.username

    class Meta(AbstractUser.Meta):
        verbose_name = '博客用户'
        verbose_name_plural = '博客用户'