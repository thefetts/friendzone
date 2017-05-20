from django.db import models


class Friend(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
