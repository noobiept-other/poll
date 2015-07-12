"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
"""
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url( r'^$', 'poll.views.home', name= 'home' ),
    url( r'^add_poll$', 'poll.views.add_poll', name= 'add_poll' ),
    url( r'^poll/(?P<pollId>\d+)$', 'poll.views.show_poll', name= 'show_poll' ),
    url( r'^poll/(?P<pollId>\d+)/results$', 'poll.views.results', name= 'results' ),

    url( r'^accounts/login$', 'django.contrib.auth.views.login', { 'template_name': 'accounts/login.html' }, name= 'login' ),
    url( r'^accounts/logout$', 'django.contrib.auth.views.logout', name= 'logout' ),
    url( r'^accounts/new$', 'poll.views.new_account', name= 'new_account' ),
    url( r'^accounts/change_password$', 'django.contrib.auth.views.password_change', { 'template_name': 'accounts/change_password.html', 'post_change_redirect': '/' }, name= 'change_password' ),
    url( r'^accounts/user/(?P<username>\w+)$', 'poll.views.user_page', name= 'user_page' ),

    url( r'^accounts/', include( 'accounts.urls', namespace= 'accounts', app_name= 'accounts' ) ),
    url( r'^admin/', include( admin.site.urls ) ),
]
