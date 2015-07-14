"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
"""
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url( r'^$', 'poll.views.home', name= 'home' ),
    url( r'^(?P<pageNumber>\d+)$', 'poll.views.home', name= 'home' ),
    url( r'^add_poll$', 'poll.views.add_poll', name= 'add_poll' ),
    url( r'^poll/(?P<pollId>\d+)$', 'poll.views.show_poll', name= 'show_poll' ),
    url( r'^poll/(?P<pollId>\d+)/results$', 'poll.views.results', name= 'results' ),
    url( r'^poll/all/(?P<username>\w+)$', 'poll.views.all_polls', name= 'all_polls' ),

    url( r'^accounts/', include( 'accounts.urls', namespace= 'accounts', app_name= 'accounts' ) ),
    url( r'^admin/', include( admin.site.urls ) ),
]
