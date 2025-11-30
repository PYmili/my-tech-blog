from django.db import models
from django.utils import timezone

from anonymous_users.models import AnonymousUser
from blog_post.models import Post


class Comment(models.Model):
    """评论模型"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="所属文章")
    author = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE, verbose_name="评论者")

    content = models.TextField(verbose_name="评论内容")
    created_time = models.DateTimeField(default=timezone.now, verbose_name="评论时间")

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"
        # 评论按时间正序排列
        ordering = ['created_time']

    def __str__(self):
        return f'Comment by {self.author} on {self.post.title}'