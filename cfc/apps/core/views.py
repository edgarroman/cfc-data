from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from cfc.apps.core.models import Game
import datetime
from itertools import groupby
from collections import defaultdict, OrderedDict
from django.views.decorators.clickjacking import xframe_options_exempt

# Number of days to show
DAYSTIMEWINDOW = 14

def extract_field(game):
    return game.field

@xframe_options_exempt
def home(request):

    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    context = dict()

    today = datetime.datetime.now()
    days = OrderedDict()
    for single_date in (today + datetime.timedelta(n) for n in range(DAYSTIMEWINDOW-today.weekday())):
        games_in_day = Game.objects.filter(schedule__date=single_date,field__cfc_home_field=True).order_by('field__name','schedule')

        if games_in_day:
            games_on_field_per_day = OrderedDict()
            for field, games_on_field in groupby(games_in_day, key=extract_field):
                game_list = []
                for game in games_on_field:
                    game_list.append(game)
                games_on_field_per_day[field] = game_list
            days[single_date] = dict(games_on_field_per_day)

    context['days'] =  days

    return render(request, 'home.html', context)
