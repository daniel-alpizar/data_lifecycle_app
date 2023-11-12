from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    home_store = models.IntegerField(blank=False, null=False, default=1, editable=False)

    def __str__(self):
        return f'{self.user.username}'