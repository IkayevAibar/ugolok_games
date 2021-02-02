from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.utils.translation import gettext_lazy as _
import os
from django.core.cache import cache 
from django.contrib.auth.models import Group
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator


class Timer(models.Model):
    game = models.ForeignKey('Game', related_name='gametimer', on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=30,blank=True, null=True)
    status = models.CharField(max_length=5,blank=True, null=True)
    message = models.CharField(max_length=30,blank=True, null=True)
    start_seconds = models.IntegerField(_("start_seconds"),blank=True, null=True)
    seconds_elapsed = models.IntegerField(_("seconds_elapsed"),blank=True, null=True)
    seconds_remaining = models.IntegerField(_("seconds_remaining"),blank=True, null=True)

    def __str__(self):
        return (str(self.start_seconds)+ " - " + str(self.seconds_elapsed) + " = " + str(self.seconds_remaining))

class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)


class Player(AbstractUser):
    status=models.CharField(_("status"), max_length=50,blank=True, null=True)
    email=models.EmailField( max_length=254,blank=True, null=True)
    first_name=None
    last_name=None

class Game(models.Model):
    # ecology = models.IntegerField('Экология',default=100,blank=True, null=True)
    creator_id = models.ForeignKey('Player', related_name='creator', on_delete=models.CASCADE,blank=True, null=True)

class Round(models.Model):
    name = models.CharField(_("Имя Раунда"), max_length=50 ,blank=True, null=True)
    ecology = models.IntegerField('Экология',default=100,blank=True, null=True)
    game = models.ForeignKey('Game', related_name='gameround', on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Country(models.Model):
    game = models.ForeignKey('Game', related_name='Game', on_delete=models.CASCADE)
    name = models.CharField('ИМЯ СТРАНЫ', max_length=150,blank=True, null=True)
    budget = models.IntegerField('БЮДЖЕТ СТРАНЫ',blank=True, null=True)
    technology = models.BooleanField('Ядерная технология',default=False,blank=True, null=True)
    rockets = models.IntegerField('Количество ракет', default=0, blank=True, null=True)
    president = models.ForeignKey('Player', related_name='Player', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    

class City(models.Model):
    country = models.ForeignKey('Country', related_name='Country', on_delete=models.CASCADE)
    name = models.CharField('ИМЯ ГОРОДА', max_length=150,blank=True, null=True)
    shield = models.BooleanField('ЩИТ',default=False,blank=True, null=True)
    status = models.IntegerField('СТАТУС',blank=True, null=True)
    def __str__(self):
        return self.name
    def update_status(self,status_):
        if(status_ and self.status>0):
            self.status+=25
    



class Order(models.Model):
    round = models.ForeignKey('Round', related_name='Round', on_delete=models.CASCADE)
    country = models.ForeignKey('Country', related_name='order_for', on_delete=models.CASCADE)
    status_for_city_1 = models.BooleanField(_("статус на город1"),default=False,blank=True, null=True)
    status_for_city_2 = models.BooleanField(_("статус на город2"),default=False,blank=True, null=True)
    status_for_city_3 = models.BooleanField(_("статус на город3"),default=False,blank=True, null=True)
    status_for_city_4 = models.BooleanField(_("статус на город4"),default=False,blank=True, null=True)
    shield_for_city_1 = models.BooleanField(_("щит на город1"),default=False,blank=True, null=True)
    shield_for_city_2 = models.BooleanField(_("щит на город2"),default=False,blank=True, null=True)
    shield_for_city_3 = models.BooleanField(_("щит на город3"),default=False,blank=True, null=True)
    shield_for_city_4 = models.BooleanField(_("щит на город4"),default=False,blank=True, null=True)
    build_tech = models.BooleanField('кач ядерки',default=False,blank=True, null=True)
    buy_rockets = models.IntegerField("покупка ракетт",default=0,blank=True, null=True)
    eco_up = models.BooleanField("Улучшение экологии",default=False,blank=True, null=True)
    rockets_to = models.CharField("Города под прицелом",max_length=254,blank=True, null=True)
    saction_to = models.CharField("Страны для санкции",max_length=254,blank=True, null=True)
    order_cost = models.IntegerField("Стоимость приказа",blank=True, null=True)
    pub_date = models.DateTimeField('Дата отправки приказа',default= timezone.now)
    def __str__(self):
        return "Cost:"+str(self.order_cost)+" Time:"+str(self.pub_date.time().strftime("%H:%M:%S"))
    

