from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')

    org=models.CharField('Organization',max_length=128,blank=True)

    telephone=models.CharField('phone',max_length=50,blank=True)

    class Meta:
        verbose_name='Usr Profile'

    def __str__(self):
        return  "{}'s Profile".format(self.user.__str__())