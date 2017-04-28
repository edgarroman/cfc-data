from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from cfc.apps.core.models import Game
import datetime
from itertools import groupby
from collections import defaultdict
from django.views.decorators.clickjacking import xframe_options_exempt

DAYSTIMEWINDOW = 7
#DAYSTIMEWINDOW = 90

def extract_date(game):
    return game.schedule.date()

def extract_field(game):
    return game.field

@xframe_options_exempt
def home(request):

    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    context = dict()

    now_day = datetime.datetime.now()
#    now_day = datetime.datetime(2016,9,1)
    delta = datetime.timedelta(DAYSTIMEWINDOW-now_day.weekday())
    next_weekend = now_day + delta
    print ("next_weekend = %s" % next_weekend)
    club = 'CFC'

    games = Game.objects.filter(field__cfc_home_field=True,
        schedule__gt=now_day,
        schedule__lt=next_weekend).order_by('schedule','field')

    print("===================================")
    for game in games:
        print (str(game) + ' - ' + str(game.home_team) + ' - '+ str(game.field))

#    days = { t: list(g) for t, g in groupby(games, key=extract_date) }

    days = defaultdict(dict)
    for day, games_in_day in groupby(games, key=extract_date):

        games_on_field_per_day = defaultdict(list)

        for field, games_on_field in groupby(games_in_day, key=extract_field):

            for game in games_on_field:
                games_on_field_per_day[field].append(game)

        days[day] = dict(games_on_field_per_day)

    #########################################################################
    # Validation

#    print('>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<')
#    pp.pprint(days)
    context['days'] =  dict(days)

    return render(request, 'home.html', context)
    #return HttpResponse('Hello')

#set([d.date() for d in date_list])
