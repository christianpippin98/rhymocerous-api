from django.db import models
from .poet import Poet


class Poem(models.Model):
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=10000)
    poet = models.ForeignKey(Poet, on_delete=models.DO_NOTHING)
    createdAt = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ("createdAt",)

    def __str__(self):
        return self.name