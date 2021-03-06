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
    club = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    squad = models.CharField(max_length=255, blank=True)
    age_division = models.CharField(max_length=255, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    league_key = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Field(TimeStampedModel):
    name = models.CharField(max_length=255)
    cfc_home_field = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class LeagueField(TimeStampedModel):
    name = models.CharField(max_length=255)
    league_key = models.CharField(max_length=255, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Game(TimeStampedModel):
    home_team = models.ForeignKey(Team, related_name="home", on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name="away", on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    schedule = models.DateTimeField()
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    league_key = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return (
            self.schedule.strftime("%m/%d %I:%M")
            + " - "
            + str(self.home_team)
            + " vs. "
            + str(self.away_team)
        )

