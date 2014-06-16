from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect

import re

from poll.models import Poll, Option

def home( request ):

    context = {
        'polls': Poll.objects.all()
    }

    return render( request, 'home.html', context )


def add_poll( request ):

    errors = []

    if request.method == 'POST':

        word = re.compile( r'\s*\w+\s*' )
        title = request.POST.get( 'title', '' )

        if not title or not word.search( title ):
            errors.append( 'Need to add a title.' )

        else:
            count = 0
            options = []

            for key, value in request.POST.iteritems():

                if key.startswith( 'option' ):

                    if word.search( value ):
                        count += 1
                        options.append( value )

            if count < 2:
                errors.append( 'Need 2 or more options.' )

            else:
                poll = Poll( title= title )
                poll.save()

                for optionText in options:

                    poll.option_set.create( text= optionText )

                return HttpResponseRedirect( poll.get_url() )

    context = {
        'errors': errors,
        'initialOptions': range( 1, 4 )
    }

    return render( request, 'add_poll.html', context )

def show_poll( request, pollId ):

    try:
        poll = Poll.objects.get( id= pollId )

    except Poll.DoesNotExist:
        raise Http404( "Invalid poll id." )

    errors = []

    if request.method == 'POST':

        optionId = request.POST.get( 'option', '' )

        try:
            selectedOption = poll.option_set.get( id= optionId )

        except Option.DoesNotExist:
            errors.append( "Selected option doesn't exist." )

        else:
            selectedOption.votes_count += 1
            selectedOption.save()

            return HttpResponseRedirect( poll.get_result_url() )

    context = {
        'poll': poll,
        'errors': errors
    }

    return render( request, 'show_poll.html', context )

def results( request, pollId ):

    try:
        poll = Poll.objects.get( id= pollId )

    except Poll.DoesNotExist:
        raise Http404( "Invalid poll id." )

    context = {
        'poll': poll
    }

    return render( request, 'results.html', context )

