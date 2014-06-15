from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect

import re

from poll.models import Poll

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
            position = 1
            count = 0
            options = []

                #HERE you can have like option1 and option3 but not option2
            while True:
                optionId = 'option{}'.format( position )

                option = request.POST.get( optionId, '' )

                if not option or not word.search( option ):
                    break

                else:

                    position += 1
                    count += 1
                    options.append( option )

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
        raise Http404

    context = {
        'poll': poll
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


def vote( request, pollId ):

    try:
        poll = Poll.objects.get( id= pollId )

    except Poll.DoesNotExist:
        raise Http404( "Invalid poll id." )


    if request.method == 'POST':

        optionId = request.POST.get( 'option', '' )

        try:
            selectedOption = poll.option_set.get( id= optionId )

        except Poll.DoesNotExist:
            return HttpResponseRedirect( poll.get_url() )   #HERE add error message

        selectedOption.votes_count += 1
        selectedOption.save()

        return HttpResponseRedirect( poll.get_result_url() )

    return HttpResponseRedirect( poll.get_url() )