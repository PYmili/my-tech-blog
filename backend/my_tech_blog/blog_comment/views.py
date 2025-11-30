from django.core.paginator import Paginator, EmptyPage
from django.forms import model_to_dict
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from anonymous_users.models import AnonymousUser
from blog_comment.models import Comment
from blog_post.models import Post
from my_tech_blog import SensitiveWordCheckInstance


class CommentPostView(APIView):
    """评论文章的视图"""

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        评论文章
        :param request: Request
        :param args: Arguments
        :param kwargs: Kwargs
        :return: Response
        """
        post_id = request.data.get('id', None)
        content = request.data.get('content', None)
        fingerprint = request.headers.get('X-Fingerprint', None)
        if not post_id or not fingerprint or not content:
            return Response({'detail': '参数残缺'}, status=status.HTTP_400_BAD_REQUEST)

        # 违禁词检测
        if SensitiveWordCheckInstance.check(content):
            return Response({'detail': '评论违规！出现违禁词！'}, status=status.HTTP_400_BAD_REQUEST)

        # 查询文章
        post = Post.objects.filter(id=post_id).first()
        if not post:
            return Response({'detail': '文章不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        # 查询访客
        anonymous_user = AnonymousUser.objects.filter(browser_fingerprint=fingerprint).first()
        if not anonymous_user:
            return Response({'detail': '访客不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.filter(post=post, author=anonymous_user)
        if comment.exists():
           return Response({'detail': '不能重复评论！'}, status=status.HTTP_400_BAD_REQUEST)

        new_comment = Comment.objects.create(post=post, author=anonymous_user, content=content)
        new_comment.save()

        return Response({'detail': '评论成功！'}, status=status.HTTP_200_OK)


class CommentListView(APIView):
    """评论列表视图"""

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        """
        获取评论的列表
        :param request: Request
        :param args: Arguments
        :param kwargs: Kwargs
        :return: Response
        """
        # 页码，页数
        try:
            page = int(request.GET.get('page', 1))
            size = int(request.GET.get('size', 10))
        except ValueError:
            return Response({'detail': '参数错误！'}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.all()
        # 处理页
        paginator = Paginator(comment, size)
        try:
            comments = paginator.page(page)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        data = []
        for c in comments:
            item = model_to_dict(c)
            item['author'] = model_to_dict(AnonymousUser.objects.get(id=item['author']))
            data.append(item)

        return Response({
            'total': comment.count(),
            'list': data
        }, status=status.HTTP_200_OK)