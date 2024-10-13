"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from apis import views
from apis.functions import user, game
urlpatterns = [
    path('admin/', admin.site.urls),
    # re_path('show_res', views.show_res, name = 'show_res'),
    re_path('userRegister', user.userRegister, name = 'userRegister'),
    re_path('userLogin', user.userLogin, name = 'userLogin'),
    re_path('userAlter', user.userAlter, name = 'userAlter'),
    re_path('userAddGame', user.userAddGame, name = 'userAddGame'),
    re_path('userAddPublisher', user.userAddPublisher, name = 'userAddPublisher'),
    re_path('userBuyGame', user.userBuyGame, name = 'userBuyGame'),
    re_path('gameSearch', game.gameSearch, name = 'gameSearch'),
    re_path('get-async-routes', views.get_async_routes, name = 'get-async-routes'),
    re_path('refresh-token', views.refresh_token, name = 'refresh-token'),
    re_path('modify', views.modify, name = 'modify'),
    re_path('query', views.query, name = 'query'),
]