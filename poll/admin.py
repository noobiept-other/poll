from django.contrib import admin

from poll.models import Poll, Option


class OptionInline( admin.TabularInline ):

    model = Option
    extra = 4


class PollAdmin( admin.ModelAdmin ):

    inlines = [ OptionInline ]
    list_display = ( 'title', 'date_created', 'get_total_votes' )
    search_fields = [ 'title' ]
    date_hierarchy = 'date_created'

admin.site.register( Poll, PollAdmin )


class OptionAdmin( admin.ModelAdmin ):

    list_display = ( 'id', 'poll', 'text', 'votes_count' )

admin.site.register( Option, OptionAdmin )

