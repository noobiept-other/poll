from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url( r'^$', 'poll.views.home', name= 'home' ),
    url( r'^add_poll$', 'poll.views.add_poll', name= 'add_poll' ),
    url( r'^poll/(?P<pollId>\d+)$', 'poll.views.show_poll', name= 'show_poll' ),
    url( r'^poll/(?P<pollId>\d+)/results$', 'poll.views.results', name= 'results' ),

    url( r'^admin/', include( admin.site.urls ) ),
)
