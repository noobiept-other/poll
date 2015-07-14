from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings

import re
import math

from poll.models import Poll, Option, Vote, POLL_TITLE_LENGTH, OPTION_TEXT_LENGTH
from poll import utilities


def home( request, pageNumber= 0 ):

    title = 'All polls'
    selected = 'all_selected'
    filterPolls = request.GET.get( 'filter', '' )

    if request.user.is_authenticated():

        if filterPolls == 'already_voted':
            polls = Poll.objects.filter( vote__voter= request.user )
            title = 'Already voted polls'
            selected = 'voted_selected'

        elif filterPolls == 'not_voted':
            polls = Poll.objects.exclude( vote__voter= request.user )
            title = 'Not voted polls'
            selected = 'not_voted_selected'

        else:
            polls = Poll.objects.all()

    else:
        polls = Poll.objects.all()


    pollsPerPage = settings.POLLS_PER_PAGE
    pageNumber = int( pageNumber )
    startPoll = pageNumber * pollsPerPage
    pollsCount = polls.count()
    totalPages = math.ceil( pollsCount / pollsPerPage )

    if startPoll > pollsCount:
        raise Http404( "Invalid page." )

    polls = polls[ startPoll : startPoll + pollsPerPage ]

    context = {
        'title': title,
        'polls': polls,
        'page': pageNumber,
        selected: True,
        'pages_list': range( 0, totalPages ),
        'filter': filterPolls
    }
    utilities.get_message( request, context )

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
        'initial_options': range( 1, 4 ),
        'title_length': POLL_TITLE_LENGTH,
        'option_length': OPTION_TEXT_LENGTH
    }

    return render( request, 'add_poll.html', context )


@login_required
def remove_poll_confirm( request, pollId ):

    try:
        poll = request.user.poll_set.get( id= pollId )

    except Poll.DoesNotExist:
        raise Http404( "Didn't find the poll." )

    context = {
        'poll': poll,
        'next': request.GET.get( 'next', '/' )
    }

    return render( request, 'confirm_remove_poll.html', context )


@login_required
def remove_poll( request, pollId ):

    try:
        poll = request.user.poll_set.get( id= pollId )

    except Poll.DoesNotExist:
        raise Http404( "Didn't find the poll." )

    utilities.set_message( request, "'{}' poll removed!".format( poll.title ) )
    poll.delete()

    nextUrl = request.GET.get( 'next', '/' )

    return HttpResponseRedirect( nextUrl )


@login_required
def open_close_poll_confirm( request, pollId ):

    try:
        poll = request.user.poll_set.get( id= pollId )

    except Poll.DoesNotExist:
        raise Http404( "Didn't find the poll." )

    context = {
        'poll': poll,
        'next': request.GET.get( 'next', '/' )
    }

    return render( request, 'confirm_open_close_poll.html', context )


@login_required
def open_close_poll( request, pollId ):

    try:
        poll = request.user.poll_set.get( id= pollId )

    except Poll.DoesNotExist:
        raise Http404( "Didn't find the poll." )

    poll.is_opened = not poll.is_opened
    poll.save( update_fields= [ 'is_opened' ] )

    if poll.is_opened:
        message = "'{}' is now opened.".format( poll.title )

    else:
        message = "'{}' is now closed.".format( poll.title )

    utilities.set_message( request, message )

    nextUrl = request.GET.get( 'next', '/' )

    return HttpResponseRedirect( nextUrl )


@login_required
def vote_poll( request, pollId ):

    try:
        poll = Poll.objects.get( id= pollId )

    except Poll.DoesNotExist:
        raise Http404( "Invalid poll id." )


    if not poll.is_opened:
        utilities.set_message( request, 'Poll is closed!' )
        return HttpResponseRedirect( poll.get_result_url() )


    errors = []

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

        # already has voted, redirect to the results page
    else:
        return HttpResponseRedirect( poll.get_result_url() )

    context = {
        'poll': poll,
        'errors': errors
    }

    return render( request, 'vote_poll.html', context )


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
        'options': poll.option_set.order_by( '-votes_count' ),
        'total_votes': total_votes,
        'has_voted': has_voted
    }
    utilities.get_message( request, context )

    return render( request, 'results.html', context )


def all_polls( request, username ):

    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "Didn't find the user." )

    context = {
        'pageUser': user,
        'polls': user.poll_set.all()
    }
    utilities.get_message( request, context )

    return render( request, 'all_polls.html', context )