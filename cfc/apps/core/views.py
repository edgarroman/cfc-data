from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from cfc.apps.core.models import Game
import datetime
from itertools import groupby

#DAYSTIMEWINDOW = 7
DAYSTIMEWINDOW = 70

def extract_date(game):
    return game.schedule.date()

def extract_field(game):
    return game.field

def home(request):

    context = dict()

#    now_day = datetime.datetime.now()
    now_day = datetime.datetime(2016,9,1)
    delta = datetime.timedelta(DAYSTIMEWINDOW-now_day.weekday())
    next_weekend = datetime.datetime.now() + delta
    club = 'CFC'

    games = Game.objects.filter(home_team__club=club,
        schedule__gt=now_day,
        schedule__lt=next_weekend).order_by('schedule','field')

    days = dict((t,list(g)) for t, g in groupby(games, key=extract_date))

    total = dict()
    for day,games in days.items():
        fields = dict((f,list(g)) for f,g in groupby(games, key=extract_field))
        print("======>>>> Day = %s, Field = %s" % (day,fields))
        total[day] = fields
    print (total)
    context['days'] =  total


    return render(request, 'home.html', context)
    #return HttpResponse('Hello')

#set([d.date() for d in date_list])
