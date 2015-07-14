"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
"""
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
        # home - list of all the polls created
    url( r'^$', 'poll.views.home', name= 'home' ),
    url( r'^(?P<pageNumber>\d+)$', 'poll.views.home', name= 'home' ),

        # add poll
    url( r'^poll/add$', 'poll.views.add_poll', name= 'add_poll' ),

        # remove poll
    url( r'^poll/remove/(?P<pollId>\d+)/confirm$', 'poll.views.remove_poll_confirm', name= 'remove_poll_confirm' ),
    url( r'^poll/remove/(?P<pollId>\d+)$', 'poll.views.remove_poll', name= 'remove_poll' ),

        # open/close poll
    url( r'^poll/open_close/(?P<pollId>\d+)/confirm$', 'poll.views.open_close_poll_confirm', name= 'open_close_poll_confirm' ),
    url( r'^poll/open_close/(?P<pollId>\d+)$', 'poll.views.open_close_poll', name= 'open_close_poll' ),

        # vote in poll
    url( r'^poll/(?P<pollId>\d+)$', 'poll.views.vote_poll', name= 'vote_poll' ),

        # show the results of a poll
    url( r'^poll/(?P<pollId>\d+)/results$', 'poll.views.results', name= 'results' ),

        # show all the polls of a user
    url( r'^poll/all/(?P<username>\w+)$', 'poll.views.all_polls', name= 'all_polls' ),


    url( r'^accounts/', include( 'accounts.urls', namespace= 'accounts', app_name= 'accounts' ) ),
    url( r'^admin/', include( admin.site.urls ) ),
]
