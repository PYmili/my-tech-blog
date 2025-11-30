from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models

from anonymous_users.models import AnonymousUser

User = get_user_model()


class Category(models.Model):
    """文章分类"""

    name = models.CharField(max_length=100, unique=True, verbose_name="分类名称")
    description = models.TextField(blank=True, verbose_name="分类描述")

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """文章标签"""

    name = models.CharField(max_length=100, unique=True, verbose_name="标签名称")

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    """文章模型"""

    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
    ]

    # 标题
    title = models.CharField(max_length=200, verbose_name="标题")
    # 作者
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name="作者")
    # 存储原始 Markdown 内容
    content_markdown = models.TextField(verbose_name="Markdown 内容")
    # 摘要
    excerpt = models.TextField(blank=True, max_length=300, verbose_name="摘要")
    # 状态
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="状态")

    created_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    # 发布时间
    published_time = models.DateTimeField(null=True, blank=True, verbose_name="发布时间")
    # 分类
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts',
                                 verbose_name="分类")
    # 标签
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name="标签")

    # 阅读量统计
    views = models.PositiveIntegerField(default=0, verbose_name="阅读量")
    # 点赞数
    stars = models.PositiveIntegerField(default=0, verbose_name="点赞数")

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
        # 默认按创建时间倒序排列
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 如果状态变为 published 且 published_time 为空，则设置发布时间
        if self.status == 'published' and not self.published_time:
            self.published_time = timezone.now()
        super().save(*args, **kwargs)


class PostViewRecord(models.Model):
    """文章浏览记录（唯一约束防重复数据）"""
    visitor = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE, related_name='viewed_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_views')
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name="浏览时间")

    class Meta:
        verbose_name = "浏览记录"
        verbose_name_plural = "浏览记录"
        # 保证每人每篇文章只有一条记录
        unique_together = ['visitor', 'post']
        # 加速 exists 查询
        indexes = [models.Index(fields=['visitor', 'post'])]

    def __str__(self):
        return f"{self.visitor.nickname} 浏览了 {self.post.title}"


class PostLikeRecord(models.Model):
    """文章点赞记录（唯一约束防重复点赞）"""
    visitor = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE, related_name='liked_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    liked_at = models.DateTimeField(auto_now_add=True, verbose_name="点赞时间")

    class Meta:
        verbose_name = "点赞记录"
        verbose_name_plural = "点赞记录"
        # 防重复
        unique_together = ['visitor', 'post']
        indexes = [models.Index(fields=['visitor', 'post'])]

    def __str__(self):
        return f"{self.visitor.nickname} 点赞了 {self.post.title}"
