from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

import re

from poll.models import Poll, Option, Vote


def home( request ):

    title = 'All polls'

    if request.user.is_authenticated():

        filterPolls = request.GET.get( 'filter', '' )

        if filterPolls == 'already_voted':
            polls = Poll.objects.filter( vote__voter= request.user )
            title = 'Already voted polls'

        elif filterPolls == 'not_voted':
            polls = Poll.objects.exclude( vote__voter= request.user )
            title = 'Not voted polls'

        else:
            polls = Poll.objects.all()

    else:
        polls = Poll.objects.all()

    context = {
        'polls': polls,
        'title': title
    }

    return render( request, 'home.html', context )


@login_required
def add_poll( request ):

    errors = []

    if request.method == 'POST':

        word = re.compile( r'\s*\w+\s*' )
        title = request.POST.get( 'title', '' )

        if not title or not word.search( title ):
            errors.append( 'Need to add a title.' )

        else:
            single_choice_str = request.POST.get( 'is_single_choice', '' )
            is_single_choice = True

            if not single_choice_str:
                is_single_choice = False


            count = 0
            options = []

            for key, value in request.POST.items():

                if key.startswith( 'option' ):

                    if word.search( value ):
                        count += 1
                        options.append({
                            'key': key,
                            'value':value
                        })

            if count < 2:
                errors.append( 'Need 2 or more options.' )

            else:
                poll = Poll( user= request.user, title= title, is_single_choice= is_single_choice )
                poll.save()

                def sortById( element ):

                    theKey = element[ 'key' ]
                    theId = re.match( r'\w+(?P<id>\d+)', theKey )
                    return theId.group( 'id' )

                options.sort( key= sortById )

                for aOption in options:

                    poll.option_set.create( text= aOption[ 'value' ] )

                return HttpResponseRedirect( poll.get_url() )

    context = {
        'errors': errors,
        'initialOptions': range( 1, 4 )
    }

    return render( request, 'add_poll.html', context )


@login_required
def show_poll( request, pollId ):

    try:
        poll = Poll.objects.get( id= pollId )

    except Poll.DoesNotExist:
        raise Http404( "Invalid poll id." )

    errors = []
    has_voted = False

    try:
        Vote.objects.get( poll= poll, voter= request.user )

    except Vote.DoesNotExist:

        if request.method == 'POST':
            try:
                optionsId = request.POST.getlist( 'options' )

            except KeyError:
                errors.append( "Need to send the options." )

            else:
                vote = Vote( poll= poll, voter= request.user )
                vote.save()

                for option in optionsId:

                    try:
                        selectedOption = poll.option_set.get( id= option )

                    except Option.DoesNotExist:
                        pass    # just ignore

                    else:
                        selectedOption.votes_count += 1
                        selectedOption.save()


                return HttpResponseRedirect( poll.get_result_url() )

    else:
        has_voted = True

    context = {
        'poll': poll,
        'errors': errors,
        'has_voted': has_voted
    }

    return render( request, 'show_poll.html', context )


def results( request, pollId ):

    try:
        poll = Poll.objects.get( id= pollId )

    except Poll.DoesNotExist:
        raise Http404( "Invalid poll id." )

    total_votes = poll.get_total_votes()
    has_voted = False

    if request.user.is_authenticated():
        has_voted = poll.has_voted( request.user )

    context = {
        'poll': poll,
        'total_votes': total_votes,
        'has_voted': has_voted
    }

    return render( request, 'results.html', context )
