from django.contrib import admin
from .models import *
import datetime

# Register your models here.
admin.site.register(LeagueField)
admin.site.register(Person)
admin.site.register(League)

class GameWeekListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Game Week'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'club'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('NextWeekend', 'Next Weekend'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'NextWeekend':
            now_day = datetime.datetime.now()
            delta = datetime.timedelta(7-now_day.weekday())
            next_weekend = datetime.datetime.now() + delta
            return queryset.filter(schedule__gt=now_day,schedule__lt=next_weekend)

class GameTeamFilter(admin.SimpleListFilter):
    title = 'CFC Team'
    parameter_name = 'team'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        teams = Team.objects.filter(club='CFC')
        return [(i.id,i) for i in teams]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        return queryset.filter(id=self.value())

class GameAdmin(admin.ModelAdmin):
    list_display = ('schedule','league', 'home_team','away_team','field')
    list_filter = ('field__cfc_home_field',GameWeekListFilter,'home_team__name')
    search_fields = ['home_team__name','away_team__name']
admin.site.register(Game,GameAdmin)

class TeamClubListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Team Club'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'club'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('CFC', 'CapitalFC'),
            ('Other', 'Other'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'CFC':
            return queryset.filter(club='CFC')
        if self.value() == '90s':
            return queryset.filter(club != 'CFC')

class TeamAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','club', 'league','age_division','league_key','url')
    list_filter = (TeamClubListFilter,'league','age_division')

admin.site.register(Team,TeamAdmin)

class FieldAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name','cfc_home_field')
admin.site.register(Field,FieldAdmin)

