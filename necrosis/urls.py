"""
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from . import views
from . import api


router = routers.DefaultRouter()
router.register(r'api2', api.ApiViewset, base_name='api_image_upload')

app_name = 'necrosis'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cbsdscore/$', views.cbsdscore, name='cbsdscore'),
    url(r'^upload/$', views.uploadimage, name='upload'),
    url(r'^downloadcsv/$', views.downloadcsv, name='downloadcsv'),
    url(r'^downloadzippedfile/$', views.downloadzippedfolder, name='downloadzippedfile'),
    url(r'^api/$', api.upload_image, name='uploadimage')
]
urlpatterns+= router.urls