from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField()
    note_text = models.CharField(max_length=500)

    def __str__(self):
        return self.note_text

