from django.db import models
from django.utils import timezone


class AnonymousUser(models.Model):
    """存储匿名用户信息。"""

    browser_fingerprint = models.CharField(max_length=128, unique=True, verbose_name="浏览器指纹哈希")
    nickname = models.CharField(max_length=50, unique=True, verbose_name="匿名昵称")
    first_seen = models.DateTimeField(default=timezone.now, verbose_name="首次访问时间")

    class Meta:
        verbose_name = "匿名用户"
        verbose_name_plural = "匿名用户"

    def __str__(self):
        return f"{self.nickname} ({self.browser_fingerprint[:10]}...)"
