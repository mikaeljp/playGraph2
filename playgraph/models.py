from django.db import models


class BggUser(models.Model):
    """
    The BggUser model represents user objects on bgg rather than a local django user object.
    There are no permissions associated with it as BGG will only provide public data via its api
    """
    id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    avatar_link = models.CharField(max_length=255, blank=True)
    year_registered = models.IntegerField(blank=True)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class BggPlay(models.Model):
    """
    The BggPlay model represents individual game plays by a BggUser
    """