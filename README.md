# bsteam

模仿steam的一个项目，可以参考steamdb，使用vue+element plus+pure admin lite+django+mysql开发，实现了<待实现>等功能。

# pure admin

建议看 <https://pure-admin.github.io/pure-admin-doc> 教程

# django

可以看 <https://www.runoob.com/django/django-tutorial.html> 教程
实际使用的地方比较少，教程仅供参考

# how to run

1. 配置环境

#### 首先是前端，即pure admin lite

```
cd lite
pnpm install # npm也行，但是推荐pnpm，怎么安装pnpm自行百度
```

#### 然后是后端，即django，建议用conda创建环境

```shell
conda create -n bsteam python=3.12
conda activate bsteam
cd server
pip install -r requirements.txt
```

#### 最后是数据库，mysql

百度去

2.配置参数
大部分地方都配好了，有问题问syf就行
注意数据库配置，在server/server/settings.py下

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'su',
        'PASSWORD': 'susu',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

NAME(数据库名称)、USER、PASSWORD要改成你自己的数据库配置

3. 运行

#### 前端

```shell
cd lite
pnpm run dev
```

运行起来之后，访问给出的url即可看到前端页面

#### 后端

```shell
cd server
python manage.py runserver
```

运行起来之后，后端就可以响应了




# 前端如何删除组件
src/views/<name>
src/router/modules/<name>.ts
src/router/enum.ts中对应的