"""drf_01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,re_path,include
from api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'video_set', views.VideoViewSet)




urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/(?P<version>\w+)/version/$',views.VersionView.as_view()),
    re_path(r'^api/(?P<version>\w+)/xml/$',views.XmlView.as_view()),
    re_path(r'^api/(?P<version>\w+)/sql01/$',views.Sql01View.as_view()),
    re_path(r'^api/(?P<version>\w+)/sql02/$',views.Sql02View.as_view()),

    # http://127.0.0.1:8000/api/v3/sql03/
    #针对get(查询全部数据)、post（新增一条数据）
    re_path(r'^api/(?P<version>\w+)/sql03/$',views.Sql03View.as_view({'get':'list','post':'create'})),
    # http://127.0.0.1:8000/api/v3/sql03/2/
    # 针对get（查询一条数据）、delete（删除一条数据）、put（更新一行中的全部数据）、patch（更新一行中的局部数据）
    re_path(r'^api/(?P<version>\w+)/sql03/(?P<pk>\d+)/$',views.Sql03View.as_view({'get':'retrieve','delete':'destroy','put':'update','patch':'partial_update'})),

    re_path(r'^api/(?P<version>\w+)/sql04/$',views.Sql04View.as_view({'get':'list','post':'create'})),
    re_path(r'^api/(?P<version>\w+)/sql04/(?P<pk>\d+)/$',views.Sql04View.as_view({'get':'retrieve','delete':'destroy','put':'update','patch':'partial_update'})),

    re_path(r'^api/(?P<version>\w+)/module/$',views.ModuleView.as_view()),

    re_path(r'^api/(?P<version>\w+)/module/new/$',views.ModuleNewView.as_view()),
    re_path(r'^api/(?P<version>\w+)/module/new/(?P<pk>\d+)/$',views.ModuleNewView.as_view()),

    re_path(r'^api/(?P<version>\w+)/module/set/$',views.ModuleSetView.as_view({'get':'list','post':'create'})),
    re_path(r'^api/(?P<version>\w+)/module/set/(?P<pk>\d+)/$',views.ModuleSetView.as_view({'get':'retrieve','delete':'destroy','put':'update','patch':'partial_update'})),

    re_path(r'^api/(?P<version>\w+)/video/$',views.VideoView.as_view()),
    re_path(r'^api/(?P<version>\w+)/video/(?P<pk>\d+)/$',views.VideoView.as_view()),

    re_path(r'^api/(?P<version>\w+)/',include(router.urls)),
]
