from django.core.management.base import BaseCommand, CommandError
from ...models import *
from pytz import timezone
from django.conf import settings

import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from urllib.parse import urlparse, urljoin

import logging
log = logging.getLogger(__name__)


class Command(BaseCommand):

    def _get_raw_page(self, url):
        r = requests.get(url)
        if r.status_code != 200:
            return

        pagesoup = BeautifulSoup(r.text, "html.parser")

        return pagesoup

    def _process_edp_schedule(self, teamname, url):

        pagesoup = self._get_raw_page(url)
        if not pagesoup:
            return

        #==========================================================
        # Sanity check
        page_team_name = pagesoup.select('span#ctl00_MainBody_TeamName')[0].text
        if page_team_name.lower().strip() != teamname.strip().lower():
            #print ("Team does not match page!!!!!!!!!!!!!!!!!!!!!!!")
            # return

        #==========================================================
        # Basic team info
        try:
            team = Team.objects.get(name=teamname)
        except Team.DoesNotExist:
            team = Team()

        try:
            league = League.objects.get(name='EDP')
        except League.DoesNotExist:
            league = League()
            league.name = 'EDP'
            league.save()

        team.club = 'CFC'
        team.league = league
        team.name = teamname

        gender_division = pagesoup.select('span#ctl00_MainBody_TeamGroup')[0].text
        team.age_division = gender_division.split()[1]
        team.url = url
        team.save()

        #==========================================================
        #

        # Find the table within the table
        schedt = pagesoup.find('table',{'width':'95%'}).table

        # Get list of game dates:
        game_dates = schedt.findAll('font',{'class':'PageHeading'})
        headers = schedt.findAll('tr',{'class':'HeadingC'})
        for gd,h in zip(game_dates,headers):
            #print ('!!!!!!!!!!!!!!!!!!!')
            #print ("gd = %s" % gd)
            gdata = h.next_sibling
            column1 = gdata.td
            league_key = column1.text.strip()
            #print (league_key)
            # time
            column2 = column1.next_sibling
            game_time = column2.text.strip()
            #print ("game_time = %s" % game_time)
            try:
                game_date_notz = parse(gd.text.strip() + "T" + game_time)
            except ValueError:
                #print ("Bad time found - will skip game")
                continue

            eastern=timezone('US/Eastern')
            game_date = eastern.localize(game_date_notz)
            #print (game_date)

            # home_team
            column3 = column2.next_sibling
            htname = column3.text.strip()
            ht = self._process_team(htname.lower(), htname.title(), league)
            #print (ht)

            # away_team
            column5 = column3.next_sibling.next_sibling
            atname = column5.text.strip()
            at = self._process_team(atname.lower(), atname.title(), league)
            #print (at)

            # field
            column7 = column5.next_sibling.next_sibling
            fname = column7.text.strip()
            field = self._process_field(fname.lower(), fname,league)
            #print (field)

            try:
                game = Game.objects.get(league_key=league_key)
            except Game.DoesNotExist:
                game = Game()
                game.league_key = league_key

            game.home_team = ht
            game.away_team = at
            game.field = field
            game.schedule = game_date
            game.league = league
            game.save()

    def _process_team(self, key, teamname, league = None):

        try:
            team = Team.objects.get(league_key=key)
        except Team.DoesNotExist:
            # now query for team name
            try:
                team = Team.objects.get(name=teamname)
            except Team.DoesNotExist:
                team = Team()
                team.name = teamname
            team.league_key = key

        if not team.league_key:
            team.league_key = key

        if league:
            team.league = league
        else:
            team.league = self.current_team.league
        team.name = teamname
        team.save()
        return team

    def _process_field(self, key, name, league=None):

        #print ('=====> name = %s' % name)
        try:
            lf = LeagueField.objects.get(league_key=key)
        except LeagueField.DoesNotExist:
            #print ('league field does not exist, checking alias for: "%s"' % name.strip())
            # Ok this is the first time we found this field for this league
            # now let's see if there is a predefined alias
            if name.strip() in settings.FIELD_ALIAS.keys():
                #print ('alias field does exist!!')
                # found an alias, then get the existing Field object
                try:
                    field = Field.objects.get(name=settings.FIELD_ALIAS[name])
                except Field.DoesNotExist:
                    #print ('alias field does not exist')
                    field = Field()
                    field.name = settings.FIELD_ALIAS[name]
                field.cfc_home_field = True

            else:
                field = Field()
                field.name = name.strip()
            field.save()
            #print ('createing field %s' % field)


            lf = LeagueField()
            lf.league_key=key
            if league:
                lf.league = league
            else:
                lf.league = self.current_team.league
            lf.name = name
            lf.field = field
        lf.save()

        return lf.field

    def get_demosphere_schedule(self, pagesoup):

        # parse to schedule
        gamerows = pagesoup.findAll("tr", {"class":"GameRow"})
        for game in gamerows:
            try:
                g = Game.objects.get(league_key=game['gamekey'])
            except Game.DoesNotExist:
                g = Game()
                g.league_key = game['gamekey']
                g.league = self.current_team.league

            dt = parse(game['date'] + ' ' + game['time'])
            eastern=timezone('US/Eastern')
            g.schedule = eastern.localize(dt)
            # parsing home team
            ht = self._process_team(game['team1key'], game.find('td',{'class' : 'tm1'}).text.strip())
            if ht:
                g.home_team = ht
            # parsing away team
            at = self._process_team(game['team2key'],game.find('td',{'class' : 'tm2'}).text.strip())
            if at:
                g.away_team = at

            fname = game.find('td',{'class':'facility'}).text.strip()
            f = self._process_field(game['facility'],fname)
            g.field = f

            g.save()
#            print ("saved game: %s" % g)

    def parse_league_page(self,pagesoup,urldomain, league):

        for t in pagesoup.findAll('tr',{'class':'tm-row'}):
            try:
                team = Team.objects.get(league_key=t['data-teamkey'])
                if team.url:
                    # skip if this team already has a url
                    # must do this for the WAGS site which has multiple
                    # seasons loaded
                    continue
            except Team.DoesNotExist:
                team = Team()
                team.league_key = t['data-teamkey']
            team.club = 'CFC'
            team.league = league
            team.age_division = t.td.text.strip().split()[0]
            t2 = t.td.next_sibling.next_sibling
            # 8/29/2017 - Clarified team name to be the anchor text only
            team.name = t2.a.text.strip()
            url_path = t2.a['href']
            team.url = urljoin(urldomain,url_path)
            #print ('Team: %s (%s) "%s"' % (team.name, team.age_division, team.url))
            team.save()

    def handle(self, *args, **options):
        print ('running refresh')
        print ('===================================')

        for t in settings.LEAGUE_EDP_TEAMS:
            self._process_edp_schedule(t['team'].title(),t['url'])

        print ('Done with EDP moving on to other leagues')
        for l in settings.LEAGUE_CFC_PAGES:
            print (l)
            try:
                league = League.objects.get(name=l['league'])
            except League.DoesNotExist:
                league = League()
                league.name=l['league']
                league.save()
            pagesoup = self._get_raw_page(l['url'])
            # Find root url
            parsed_uri = urlparse( l['url'] )
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            self.parse_league_page(pagesoup, domain, league)

        # Now process the database
        teams = Team.objects.filter(club="CFC")
        for team in teams:
            print ('===================================')
            #print ("Team: %s" % team)

            if not team.url:
                continue
            pagesoup = self._get_raw_page(team.url)

            if pagesoup:
                self.current_team = team
                #print ("got page")
                #team = verify_team_info(pagesoup, team)
                schedule = self.get_demosphere_schedule(pagesoup)
