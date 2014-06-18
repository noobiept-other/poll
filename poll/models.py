from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Poll( models.Model ):

    user = models.ForeignKey( User )
    title = models.CharField( max_length= 100 )
    date_created = models.DateTimeField( help_text= 'Date Created', default= lambda: timezone.localtime(timezone.now()) )
    is_single_choice = models.BooleanField( default= True )

    def get_total_votes(self):
        count = 0

        for option in self.option_set.all():
            count += option.votes_count

        return count

    def get_url(self):

        return reverse( 'show_poll', args= [ self.id ] )

    def get_result_url(self):
        return reverse( 'results', args= [ self.id ] )

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = [ '-date_created' ]


class Option( models.Model ):
    poll = models.ForeignKey( Poll )
    text = models.CharField( max_length= 20 )
    votes_count = models.PositiveIntegerField( default= 0 )

    def __unicode__(self):
        return self.text