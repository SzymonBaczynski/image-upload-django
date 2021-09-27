from django.db import models
from django.contrib.auth.models import AbstractUser

from api.models import Plan


class User(AbstractUser):
    userPlan = models.ForeignKey(Plan, on_delete=models.PROTECT, blank=False)

    def save(self, *args, **kwargs):
        try: 
            plan = self.userPlan
        except User.userPlan.RelatedObjectDoesNotExist:
            firstPlan = Plan.objects.first()
            if firstPlan:
                self.userPlan = firstPlan                
            else:
                self.userPlan =  Plan.objects.create( planName = 'Generic plan')
        super(User, self).save(*args, **kwargs)