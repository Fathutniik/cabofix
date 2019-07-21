from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from enum import Enum

from django.db import models


# Create your models here.
class Claim(models.Model):
    wait = "Ожидает выполнеиния"
    process = "Выполняется"
    ok = "Выполнено"
    vibor = [
        (wait, "Ожидает выполнеиния"),
        (process, "Выполняется"),
        (ok, "Выполнено")
    ]
    text = models.TextField()
    Imya = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authored_problems")
    likes = models.ManyToManyField(User)
    stat = models.CharField(max_length=25, choices=vibor, default=wait)

    def __str__(self):
        return self.Imya

    def counts(self):
        return self.likes.count()
