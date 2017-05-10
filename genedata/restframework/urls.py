#! /usr/bin/env python
# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import
"""restframework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers  
from rest import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

  
router = routers.DefaultRouter()  
router.register(r'users', views.UserViewSet)  
router.register(r'groups', views.GroupViewSet)  
#router.register(r'genomelists',views.GenomeList)
#router.register(r'genomedetails',views.GenomeDetail)
#router.register(r'tracklists', views.TrackList)
#router.register(r'trackdetails', views.TrackDetail)

# Wire up our API using automatic URL routing.  
# Additionally, we include login URLs for the browseable API.  
urlpatterns += [  
    url(r'^', include(router.urls)),  
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^genomelist/$', views.GenomeList.as_view(), name='GenomeList'),
    url(r'^genome/(?P<pk>[0-9]+)$', views.GenomeDetail.as_view(), name='genome-detail'),
    url(r'^tracklist/$', views.TrackList.as_view(), name='TrackList'),
    url(r'^track/(?P<pk>[0-9]+)$', views.TrackDetail.as_view(), name='track-detail'),
    url(r'^index/$', views.igv_index, name='index'),
    url(r'^genecodelist/$', views.GenecodeList.as_view(), name='GenecodeList'),
    url(r'^genecode/(?P<pk>[0-9]+)$', views.GenecodeDetail.as_view(), name='genecode-detail'), 
    url(r'^contactlist/$', views.ContactList.as_view(), name='ContactList'),
    url(r'^contact/(?P<pk>[0-9]+)$', views.ContactDetail.as_view(), name='contact-detail'), 
    url(r'^networkx/([a-zA-Z\_][0-9a-zA-Z\-\.]{0,15})/$', views.networkx_json, name="networkx"),        
    url(r'^networkx_test/$', views.network_test, name="test"),
] 

#urlpatterns = format_suffix_patterns(urlpatterns)

