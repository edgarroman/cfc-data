from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Person(TimeStampedModel):
    name = models.CharField(max_length=255)
    email = models.EmailField
    def __str__(self):
        return self.name

class League(TimeStampedModel):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Team(TimeStampedModel):
    club = models.CharField(max_length=255,blank=True)
    name = models.CharField(max_length=255)
    squad = models.CharField(max_length=255,blank=True)
    age_division = models.CharField(max_length=255, blank=True)
    league = models.ForeignKey(League)
    league_key = models.CharField(max_length=255,blank=True)
    url = models.URLField(blank=True,null=True)
    def __str__(self):
        return self.name

class Field(TimeStampedModel):
    name = models.CharField(max_length=255)
    cfc_home_field = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class LeagueField(TimeStampedModel):
    name = models.CharField(max_length=255)
    league_key = models.CharField(max_length=255,blank=True)
    league = models.ForeignKey(League)
    field = models.ForeignKey(Field)
    def __str__(self):
        return self.name

class Game(TimeStampedModel):
    home_team = models.ForeignKey(Team,related_name='home')
    away_team = models.ForeignKey(Team,related_name='away')
    field = models.ForeignKey(Field)
    schedule = models.DateTimeField()
    league = models.ForeignKey(League)
    league_key = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return (self.schedule.strftime("%m/%d %I:%M") + 
                ' - ' + 
                str(self.home_team) + 
                ' vs. ' + 
                str(self.away_team))


