# my-tech-blog
> 使用Django5 + vue3开发的个人技术博客项目

## 功能
> 以下是简单的功能描述：
1. `后台信息管理` - 管理员信息修改功能
2. `文章流量视图` - 管理员发布的总文章各项流量数据
3. `文章编辑发布` - **markdown**编辑文章，可发布文章
4. `文章分类管理` - 对分类可进行新增、删除
5. `文章公共展示` - 主页公共展示文章，且有热榜展示
6. `访客查看文章` - 访客可查看文章内容
7. `访客评论文章` - 访客可以评论文章内容
8. `访客点赞文章` - 访客可以点赞文章
9. `评论违禁检测` - 可对评论的违禁词进行检查
10. `访客信息唯一` - 访客信息根据 **浏览器指纹** 区分，可防止重复。

## 部署
> 在部署项目前，请确保安装以下环境：
> > `Python (>=3.12.x）`
> 
> > `mysql (>=8.x)`
> 
> > `nodjs (>=v22.x)`
> 
> > `pnpm (>=10.12.2)/npm (>=10.9.2)`

1. 拉取仓库项目:
```shell
git clone https://github.com/PYmili/my-tech-blog.git
cd my-tech-blog/backend/my_tech_blog
```
1. 安装`python`依赖
```shell
pip install -r .\requirements.txt
```
1. 配置mysql数据库并迁移项目模型
```shell
# 根目录创建.env文件
DB_NAME=my_tech_blog
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```
```shell
python .\manage.py makemigrations
python .\manage.py migrate
```
1. 运行后端:
```shell
python .\manage.py runserver
```
1. 配置前端`vue3`环境，并运行
```shell
cd ..\..\frontend\my-tech-blog
pnpm install
pnpm run dev
```
    **若使用npm或yarn，请使用其命令，替换pnpm**
