from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.template.defaultfilters import truncatechars

from accounts.models import Account


POLL_TITLE_LENGTH = 100
OPTION_TEXT_LENGTH = 50


class Poll( models.Model ):

    user = models.ForeignKey( Account )
    title = models.CharField( max_length= POLL_TITLE_LENGTH )
    date_created = models.DateTimeField( help_text= 'Date Created', default= timezone.now )
    is_single_choice = models.BooleanField( default= True )
    is_opened = models.BooleanField( default= True )

    def get_total_votes(self):
        count = 0

        for option in self.option_set.all():
            count += option.votes_count

        return count

    def get_url(self):
        return reverse( 'vote_poll', args= [ self.id ] )

    def get_result_url(self):
        return reverse( 'results', args= [ self.id ] )

    def has_voted(self, user):
        try:
            self.vote_set.get( voter= user )

        except Vote.DoesNotExist:
            return False

        else:
            return True

    def get_highest_vote(self):
        option = self.option_set.latest( 'votes_count' )
        total = self.get_total_votes()

        if total != 0:
            name = truncatechars( option.text, 20 )
            percentage = round( option.votes_count / total * 100 )

            return '{} {}%'.format( name, percentage )



    def __str__(self):
        return self.title

    class Meta:
        ordering = [ '-date_created' ]


class Option( models.Model ):
    poll = models.ForeignKey( Poll )
    text = models.CharField( max_length= OPTION_TEXT_LENGTH )
    votes_count = models.PositiveIntegerField( default= 0 )

    def __str__(self):
        return self.text


class Vote( models.Model ):
    poll = models.ForeignKey( Poll )
    voter = models.ForeignKey( Account, related_name= 'voter' )