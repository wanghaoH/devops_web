# -*- coding: utf-8 -*-
#Auth: liu
from django.contrib import admin
from django.urls import path, re_path
from .views import *


# urlpatterns = [
#     re_path('^login/$',Login.as_view()),
#     re_path('^index/$',index.as_view()),
# ]
urlpatterns = [
    re_path('^login/$',login,name='login'),
    re_path('^index/$',index,name='index'),
    re_path('^register/$',register,name='register'),
    re_path('^abc/$', abc, name='abc'),
    re_path('^def/$', svn_asset, name='def'),
    re_path('^jh/$', truncate, name='jh'),
    re_path('^svn_list/$', svn_list, name='svn_list')
]
