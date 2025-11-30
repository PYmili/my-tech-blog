from datetime import timedelta

from django.core.paginator import Paginator, EmptyPage
from django.db import IntegrityError
from django.db.models import Sum, F, Count
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from django.forms import model_to_dict
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from anonymous_users.models import AnonymousUser
from blog_comment.models import Comment
from blog_post.models import Post, Category, Tag, PostViewRecord, PostLikeRecord


class StatisticsView(APIView):
    """统计文章视图"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        返回统计后的数据
        :param request: Request
        :return: Response
        """
        user_posts = Post.objects.filter(author=request.user)
        # 浏览量
        views = user_posts.aggregate(total_views_sum=Sum('views')).get('total_views_sum') or 0
        # 已发布
        published = user_posts.filter(status='published').count()
        # 评论数
        comments = Comment.objects.filter(post__in=user_posts).count()
        # 点赞数
        stars = user_posts.aggregate(total_stars_sum=Sum('stars')).get('total_stars_sum') or 0

        # 构造返回数据
        data = {
            'total': user_posts.count(),
            'views': views,
            'published': published,
            'comments': comments,
            'stars': stars,
        }

        return Response(data, status=status.HTTP_200_OK)


class RecentView(APIView):
    """最近文章视图，返回前3条最新文章"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        获取最新的文章前3条
        :param request: Request
        :return: Response
        """
        user_posts = Post.objects.filter(author=request.user)
        data = []
        for i in user_posts.order_by('-created_time')[:3]:
            item = model_to_dict(i)
            item['tags'] = [t.name for t in i.tags.all()]
            item['created_time'] = i.created_time.strftime('%Y-%m-%d %H:%M:%S')
            data.append(item)
        return Response({'recentArticles': data}, status=status.HTTP_200_OK)


class PostListView(APIView):
    """文章列表视图"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        根据页数和页码获取文章列表
        :param request: Request
        :return: Response
        """
        # 页码，页数
        try:
            page = int(request.GET.get('page', 1))
            size = int(request.GET.get('size', 10))
        except ValueError:
            return Response({'detail': 'page/size 需为整数'}, status=status.HTTP_400_BAD_REQUEST)

        # 搜索关键字
        keyword = request.GET.get('keyword', '')

        post = Post.objects.all()
        if len(keyword) > 0:
            post = post.filter(title__icontains=keyword)

        # 状态
        status_param = request.GET.get('status', '')
        if len(status_param) > 0 and status_param in [i for i, j in Post.STATUS_CHOICES]:
            post = post.filter(status=status_param)

        # 处理页
        paginator = Paginator(post, size)
        try:
            posts = paginator.page(page)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        data = []
        for p in posts:
            item = model_to_dict(p)
            item['tags'] = [t.name for t in p.tags.all()]
            item['created_time'] = p.created_time.strftime('%Y-%m-%d %H:%M:%S')
            item['category'] = Category.objects.get(id=p.category.id).name
            data.append(item)

        return Response({
            'total': post.count(),
            'pages': paginator.num_pages,
            'list': data
        }, status=status.HTTP_200_OK)


class PostHotListView(APIView):
    """热度榜单视图"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        获取热度榜单（自动只返回已发布文章，按浏览量 > 点赞数，返回前10）
        :param request: Request
        :return: Response (格式与PostListView完全一致)
        """
        # 热度榜单默认只返回 status='published' 的文章
        posts_queryset = Post.objects.filter(
            status='published').order_by('-views', '-stars')[:10]

        # 数据格式化
        data = []
        for p in posts_queryset:
            item = model_to_dict(p)
            item['tags'] = [t.name for t in p.tags.all()]
            item['created_time'] = p.created_time.strftime('%Y-%m-%d %H:%M:%S')
            item['category'] = p.category.name if p.category else ''
            item['comments'] = Comment.objects.filter(post=p).count()
            data.append(item)

        # 返回
        return Response({'list': data}, status=status.HTTP_200_OK)


class PostDetailView(APIView):
    """文章详细内容"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        根据页数和页码获取文章列表
        :param request: Request
        :return: Response
        """
        # 页码，页数
        try:
            id_param = int(request.GET.get('id', ''))
        except ValueError:
            return Response({'detail': 'id 需为整数'}, status=status.HTTP_400_BAD_REQUEST)

        fingerprint = request.headers.get('X-Fingerprint', None)
        anonymous_user = None
        if fingerprint:
            # 查询访客
            anonymous_user = AnonymousUser.objects.filter(browser_fingerprint=fingerprint)
            if anonymous_user.exists():
                anonymous_user = anonymous_user.first()

        post = Post.objects.filter(id=id_param).first()
        if not post:
            return Response({'detail': '文章不存在！'}, status=status.HTTP_200_OK)

        # 查询当前文章是否被访客查看过
        if anonymous_user:
            record = PostViewRecord.objects.filter(visitor=anonymous_user, post=post).first()
            if not record:
                # 保存浏览记录
                record = PostViewRecord.objects.create(visitor=anonymous_user, post=post)
                record.save()

                # 更新views
                Post.objects.filter(id=id_param).update(views=F('views') + 1)

        data = model_to_dict(Post.objects.get(id=id_param))
        data['tags'] = [t.name for t in post.tags.all()]
        data['created_time'] = post.created_time.strftime('%Y-%m-%d %H:%M:%S')
        data['category'] = Category.objects.get(id=post.category.id).name
        data['views'] = data['views']

        return Response({
            'data': data
        }, status=status.HTTP_200_OK)


class CategoryListView(APIView):
    """分类列表视图"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        获取所有分类
        :param request: Request
        :return: Response
        """
        data = []
        for i in Category.objects.all():
            item = model_to_dict(i)
            item['count'] = Post.objects.filter(category=i).count()
            data.append(item)

        return Response({'list': data}, status=status.HTTP_200_OK)


class CategoryAddView(APIView):
    """分类新增视图"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        新增分类
        :param request: Request
        :return: Response
        """
        category = request.data.get('category', None)
        if not category:
            return Response({'detail': 'category字段不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        name = category.get('name', None)
        description = category.get('description', None)

        if not name and not description:
            return Response({'detail': '参数残缺！'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            created = Category.objects.create(name=name, description=description)
            created.save()
            return Response({'detail': '新增成功！'}, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response({'detail': '重复的分类！'}, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteView(APIView):
    """删除分类的视图"""

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        """
        删除分类的请求
        :param request: Request
        :return: Response
        """
        # 需要删除的分类名
        name = request.query_params.get('name', None)
        if not name:
            return Response({'detail': 'name是必填参数'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(name=name)
            category.delete()
            return Response({'detail': '删除成功！'}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'detail': '分类不存在！'}, status=status.HTTP_400_BAD_REQUEST)


class PostAddView(APIView):
    """添加新文章视图"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        新增文章
        :param request: Request
        :return: Response
        """
        data = request.data
        required = ('title', 'content_markdown')
        for field in required:
            if not data.get(field):
                return Response({'detail': f'{field} 不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        # 提取category，如果不存在直接返回404
        category = get_object_or_404(Category, name=data['category']) if data.get('category') else None
        # 提取tag
        tag_objs = []
        if data.get('tags'):
            # get_or_create，获取到tag或者创建tag
            tag_objs = [Tag.objects.get_or_create(name=t)[0] for t in data['tags']]

        # 创建文章
        post = Post.objects.create(
            title=data['title'],
            content_markdown=data['content_markdown'],
            excerpt=data.get('content_markdown', '')[:10],
            status=data.get('status', 'draft'),
            category=category,
            author=request.user
        )
        if tag_objs:
            for tag in tag_objs:
                post.tags.add(tag)

        return Response({'id': post.id, 'detail': '创建成功'}, status=status.HTTP_201_CREATED)


class PostDeleteView(APIView):
    """删除单篇文章"""

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        """
        删除文章
        :param request: Request
        :return: Response
        """
        post_id = request.query_params.get('id')
        if not post_id:
            return Response({'detail': '缺少文章 id'}, status=status.HTTP_400_BAD_REQUEST)

        post = get_object_or_404(Post, id=post_id, author=request.user)
        post.delete()
        return Response({'detail': '删除成功'}, status=status.HTTP_200_OK)


class PostUpdateView(APIView):
    """更新单篇文章"""

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        """
        更新文章
        :param request: Request
        :return: Response
        """
        data = request.data
        post_id = data.get('id')
        if not post_id:
            return Response({'detail': '缺少文章 id'}, status=status.HTTP_400_BAD_REQUEST)

        # 获取文章对象（必须是当前用户的文章）
        post = get_object_or_404(Post, id=post_id, author=request.user)

        # 必填字段检查
        required = ('title', 'content_markdown')
        for field in required:
            if not data.get(field):
                return Response({'detail': f'{field} 不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        # 摘要
        excerpt = data['content_markdown'][:300]

        # 处理分类（如果提供新分类则更新）
        category = None
        if data.get('category'):
            category = get_object_or_404(Category, name=data['category'])

        # 处理标签：清除旧标签，添加新标签
        if data.get('tags'):
            post.tags.clear()  # 清除所有现有标签
            tag_objs = [Tag.objects.get_or_create(name=t)[0] for t in data['tags']]
            for tag in tag_objs:
                post.tags.add(tag)

        # 更新文章内容
        post.title = data['title']
        post.content_markdown = data['content_markdown']
        post.excerpt = excerpt
        post.status = data.get('status', post.status)  # 保留原状态（如果未提供）
        if category:
            post.category = category

        post.save()
        return Response({'id': post.id, 'detail': '更新成功'}, status=status.HTTP_200_OK)


class LikePostView(APIView):
    """点赞文章视图"""

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        点赞指定的文章
        :param request: Request
        :param args: Arguments
        :param kwargs: Kwargs
        :return: Response
        """
        post_id = request.data.get('id', None)
        fingerprint = request.headers.get('X-Fingerprint', None)
        if not post_id or not fingerprint:
            return Response({'detail': '参数残缺'}, status=status.HTTP_400_BAD_REQUEST)

        # 查询文章
        post = Post.objects.filter(id=post_id).first()
        if not post:
            return Response({'detail': '文章不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        # 查询访客
        anonymous_user = AnonymousUser.objects.filter(browser_fingerprint=fingerprint).first()
        if not anonymous_user:
            return Response({'detail': '访客不存在！'}, status=status.HTTP_400_BAD_REQUEST)

        # 查询当前文章是否被访客点赞过
        record = PostLikeRecord.objects.filter(visitor=anonymous_user, post=post)
        if record.exists():
            return Response({'detail': '不能重复点赞'}, status=status.HTTP_400_BAD_REQUEST)

        # 保存点赞记录
        record = PostLikeRecord.objects.create(visitor=anonymous_user, post=post)
        record.save()

        # 更新stars
        Post.objects.filter(id=post_id).update(stars=F('stars') + 1)

        return Response({'detail': '成功!'}, status=status.HTTP_200_OK)


class TrafficStatisticsPostView(APIView):
    """流量数据统计视图"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        获取今日/本周/本月/总计访问量及环比趋势
        :param request: Request
        :return: Response
        """

        # 获取当前日期时间（带时区）
        now = timezone.now()
        today = now.date()

        # ================ 日期范围计算 ================
        # 昨日
        yesterday = today - timedelta(days=1)

        # 本周（周一到今天）
        start_of_this_week = today - timedelta(days=today.weekday())  # Monday

        # 上周（完整一周）
        start_of_last_week = start_of_this_week - timedelta(days=7)

        # 本月（1号到今天）
        start_of_this_month = today.replace(day=1)

        # 上月（完整月）
        if today.month == 1:
            start_of_last_month = today.replace(year=today.year - 1, month=12, day=1)
        else:
            start_of_last_month = today.replace(month=today.month - 1, day=1)

        # ================ 查询统计 ================
        # 今日访问
        today_views = PostViewRecord.objects.filter(viewed_at__date=today).count()

        # 昨日访问（用于环比）
        yesterday_views = PostViewRecord.objects.filter(viewed_at__date=yesterday).count()

        # 本周访问
        this_week_views = PostViewRecord.objects.filter(
            viewed_at__date__gte=start_of_this_week
        ).count()

        # 上周访问
        last_week_views = PostViewRecord.objects.filter(
            viewed_at__date__gte=start_of_last_week,
            viewed_at__date__lt=start_of_this_week  # 不包含本周
        ).count()

        # 本月访问
        this_month_views = PostViewRecord.objects.filter(
            viewed_at__date__gte=start_of_this_month
        ).count()

        # 上月访问
        last_month_views = PostViewRecord.objects.filter(
            viewed_at__date__gte=start_of_last_month,
            viewed_at__date__lt=start_of_this_month  # 不包含本月
        ).count()

        # 总访问（全站累计）
        total_views = PostViewRecord.objects.count()

        # ================ 环比计算 ================
        def calculate_trend(current, previous):
            """计算百分比变化，保留1位小数"""
            if previous == 0:
                return 100.0 if current > 0 else 0.0
            return round(((current - previous) / previous) * 100, 1)

        # ================ 组装响应 ================
        data = {
            'todayViews': today_views,
            'todayTrend': calculate_trend(today_views, yesterday_views),

            'weekViews': this_week_views,
            'weekTrend': calculate_trend(this_week_views, last_week_views),

            'monthViews': this_month_views,
            'monthTrend': calculate_trend(this_month_views, last_month_views),

            'totalViews': total_views
        }

        return Response(data, status=status.HTTP_200_OK)


class PostChartDataView(APIView):
    """
    文章图表数据接口
    提供按天、周、月三个维度的访问趋势数据
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        获取文章数据统计，并返回给前端图表需要的格式
        :param request: Request
        :return: Response
        """
        try:
            now = timezone.now()

            # 生成三个维度的数据
            chart_data = {
                'day': self._get_daily_data(now),
                'week': self._get_weekly_data(now),
                'month': self._get_monthly_data(now)
            }

            return Response({
                'code': 200,
                'msg': 'success',
                'data': {
                    'chartData': chart_data
                }
            })
        except Exception as e:
            return Response({
                'code': 500,
                'msg': f'获取图表数据失败: {str(e)}'
            })

    def _get_daily_data(self, now):
        """获取最近30天的访问数据"""
        end_date = now.date()
        start_date = end_date - timedelta(days=29)

        # 查询每日访问记录数
        daily_stats = PostViewRecord.objects.filter(
            viewed_at__date__gte=start_date,
            viewed_at__date__lte=end_date
        ).annotate(
            date=TruncDate('viewed_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

        # 转换为字典便于查找
        stats_dict = {stat['date']: stat['count'] for stat in daily_stats}

        # 生成完整的日期和数值列表（与前端mock格式一致）
        dates = []
        values = []
        for i in range(29, -1, -1):
            current_date = end_date - timedelta(days=i)
            dates.append(f"{current_date.month}/{current_date.day}")
            values.append(stats_dict.get(current_date, 0))

        return {'dates': dates, 'values': values}

    def _get_weekly_data(self, now):
        """获取最近12周的访问数据"""
        end_date = now.date()
        start_date = end_date - timedelta(weeks=11)

        # 按周统计，TruncWeek返回当周周一
        weekly_stats = PostViewRecord.objects.filter(
            viewed_at__date__gte=start_date
        ).annotate(
            week=TruncWeek('viewed_at')
        ).values('week').annotate(
            count=Count('id')
        ).order_by('week')

        # 转换为字典
        stats_dict = {stat['week'].date(): stat['count'] for stat in weekly_stats}

        dates = []
        values = []
        for i in range(11, -1, -1):
            # 计算第i周的开始日期（周一）
            week_start = (end_date - timedelta(weeks=i))
            week_start -= timedelta(days=week_start.weekday())

            dates.append(f"第{12 - i}周")
            values.append(stats_dict.get(week_start, 0))

        return {'dates': dates, 'values': values}

    def _get_monthly_data(self, now):
        """获取最近12个月的访问数据"""
        end_date = now.date()

        # 查询最近12个月的数据
        monthly_stats = PostViewRecord.objects.filter(
            viewed_at__date__gte=end_date - timedelta(days=365)
        ).annotate(
            month=TruncMonth('viewed_at')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')

        # 转换为(year, month)元组作为key
        stats_dict = {
            (stat['month'].year, stat['month'].month): stat['count']
            for stat in monthly_stats
        }

        month_names = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        dates = []
        values = []

        # 生成最近12个月的列表
        for i in range(11, -1, -1):
            # 计算目标月份
            if end_date.month - i <= 0:
                year = end_date.year - 1
                month = 12 + (end_date.month - i)
            else:
                year = end_date.year
                month = end_date.month - i

            dates.append(month_names[month - 1])
            values.append(stats_dict.get((year, month), 0))

        return {'dates': dates, 'values': values}
