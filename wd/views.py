from django.shortcuts import render
from datetime import datetime
import requests
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import *
from django import forms
from django.core.exceptions import ValidationError

# import React from 'react'

# Create your views here.
def index(request):
    return render(
        request,
        'wd/index.html',
        {
            'title':'Home Page',
            'games':Game.objects.all()
        }
    )

# def user_list(request):
#     return render(request, 'wd/user_list.html')
User = get_user_model()

def enter(request):
    return render(request, 'wd/search_chat.html')

@login_required(login_url='/login/')
def room(request, room_name):
    return render(request, 'wd/room.html', {
        'room_name': room_name
    })

@login_required(login_url='/login/')
def creategame(request):
    game = Game.objects.create(ecology=100,creator_id=request.user)
    return redirect('game',game.id)

@login_required(login_url='/login/')
def lobby(request, game_id):
    game = Game.objects.filter(id=game_id)[0]    
    countries = Country.objects.filter(game=game)
    players = Player.objects.all().exclude(is_superuser=True,is_staff=True)
    list_={}
    for country in countries:
        cities = City.objects.filter(country=country)
        city_list=[]
        for city in cities:
            city_list.append(city)
        list_[country] = city_list
        city_list={}
    if(request.POST):
        cs = Country.objects.all()
        
        for c in cs:
            if(request.POST[c.name] != None or request.POST[c.name] != 'Select one'):
                c.president=Player.objects.filter(id=request.POST[c.name])[0]
                c.save(update_fields=["president"])
    return render(request, 'wd/lobby.html', {
        'game': game,
        'cc':list_,
        'ccs':countries,
        'ps':players,
    })

@login_required(login_url='/login/')
def game(request, game_id):
    game = Game.objects.filter(id=game_id)[0]    
    countries = Country.objects.filter(game=game)
    players = Player.objects.all().exclude(is_superuser=True,is_staff=True)
    rounds = Round.objects.all()
    list_={}
    for country in countries:
        cities = City.objects.filter(country=country)
        city_list=[]
        for city in cities:
            city_list.append(city)
        list_[country] = city_list
        city_list={}
    
    return render(request, 'wd/game.html', {
        'game': game,
        'cc':list_,
        'ccs':countries,
        'rounds':rounds,
        'ps':players,
    })

class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=('round','country')


def clean_values(obj):
    field = ""
    for value in obj:
      field += str(value)+","
    return field.rstrip(",")

@login_required
def order(request,game_id):
    game = Game.objects.filter(id=game_id)[0]
    rounds = Round.objects.filter(game=game)
    mc = Country.objects.filter(president=request.user)
    if(mc.count()>0):
        ccs = Country.objects.all().exclude(president=request.user)
        cities = City.objects.all().exclude(country=mc[0])

    else:
        return redirect('wd:game',game_id)
    if(request.POST):
        form = OrderForm(request.POST)
        print(form.data)
        print(form.is_valid())
        if(form.is_valid()):
            Order.objects.create(
                country=Country.objects.filter(id=int(form.data['country']))[0],
                round=Round.objects.filter(id=int(form.data['round']))[0],
                status_for_city_1=(form.data.get('status_for_city_1')),
                status_for_city_2=(form.data.get('status_for_city_2')),
                status_for_city_3=(form.data.get('status_for_city_3')),
                status_for_city_4=(form.data.get('status_for_city_4')),
                shield_for_city_1=(form.data.get('shield_for_city_1')),
                shield_for_city_2=(form.data.get('shield_for_city_2')),
                shield_for_city_3=(form.data.get('shield_for_city_3')),
                shield_for_city_4=(form.data.get('shield_for_city_4')),
                build_tech=(form.data.get('build_tech')),
                eco_up=(form.data.get('eco_up')),
                buy_rockets=form.data.get('buy_rockets'),
                rockets_to=clean_values(form.data.getlist('rockets_to')),
                saction_to=clean_values(form.data.getlist('saction_to')),
                order_cost=form.data.get('order_cost')
            )
    else:
        form = OrderForm()

    return render(request, 'wd/order.html', {
        'game': game,
        'rounds':rounds,
        'cs':ccs,
        'cities':cities,
        'mcities':City.objects.all().filter(country=mc[0]),
        'mc':mc[0],
        'form':form
    })

from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@login_required
def orders(request,game_id):
    if(request.user.id!=1):
        return redirect("wd:game",game_id)
    game = Game.objects.filter(id=game_id)[0]
    rounds = Round.objects.filter(game=game)
    countries = Country.objects.all()
    list_=[]
    list_c={}
    for round in rounds:
        for country in countries:
            orders = Order.objects.filter(round=round,country=country).order_by("-pub_date").first()
            list_c[country]=(orders)
        list_.append(list_c)
        list_c={}
    
    return render(request, 'wd/orders.html', {
        'game': game,
        'rounds':rounds,
        'ro':list_,
    })

def status_calc(cur_,status):
    if(status and cur_>0):
        return cur_+25
    return cur_

@login_required
def apply_round(request,game_id,round_id):
    if(request.user.id!=1):
        return redirect("wd:game",game_id)
    game = Game.objects.filter(id=game_id)[0]
    round_ = Round.objects.filter(id=round_id,game=game)[0]
    countries = Country.objects.all()
    rockets_to_list = {}
    saction_to_list = {}
    list_c=[]
    for country in countries:
        orders = Order.objects.filter(round=round_,country=country).order_by("-pub_date").first()
        list_c.append(orders)
    
    print(list_c)
    for order in list_c:
        if(order!=None):
            country = Country.objects.filter(id=order.country.id).first()
            cities = City.objects.filter(country=country)
            o_l_ = [order.status_for_city_1,order.status_for_city_2,order.status_for_city_3,order.status_for_city_4]
            o_l_2 = [order.shield_for_city_1,order.shield_for_city_2,order.shield_for_city_3,order.shield_for_city_4]
            i = 0
            for city in cities:
                city.update_status(o_l_[i])
                city.shield=o_l_2[i]
                city.save(update_fields=["status","shield"]) 
                i+=1
            if(order.build_tech):
                country.technology = order.build_tech
                if(round_.ecology>0):
                    round_.ecology -= 10
            if(order.buy_rockets>0):
                if(round_.ecology>0):
                    round_.ecology -= 15*order.buy_rockets
            country.rockets += order.buy_rockets
            if(order.eco_up):
                if(round_.ecology<86):
                    round_.ecology += 15
            if(order.rockets_to!=None):
                rockets_to_list[country.id]=order.rockets_to
            if(order.saction_to!=None):
                saction_to_list[country.id]=order.saction_to
            country.budget= country.budget - order.order_cost + (cities[0].status * 3 + cities[1].status * 3 + cities[2].status * 3 + cities[3].status * 3) -  50*round((round_.ecology/10))
                
            country.save(update_fields=["technology","rockets","budget"])   
            round_.save(update_fields=["ecology"])
                
    for k,v in rockets_to_list.items():
        for c_id in v.split(','):
            country = Country.objects.filter(id=k).first()
            city = City.objects.filter(id=c_id).first()
            if(city.shield):
                city.shield = False
                city.status-=30
            else:
                city.status = 0
            country.rockets-=1
            city.save(update_fields=["shield","status"])
            country.save(update_fields=["rockets"])

    for k,v in saction_to_list.items():
        for c_id in v.split(','):
            country_from = Country.objects.filter(id=k).first()
            country_to = Country.objects.filter(id=c_id).first()
            print(country_from,country_to)
            country_to.budget-=round(country_to.budget*0.15)
            country_to.save(update_fields=["budget"])
    
                
                
    return redirect("wd:orders",game_id)


def country(request,game_id):
    game = Game.objects.filter(id=game_id).first()
    c=Country.objects.filter(game=game,president=request.user).first()
    cities = City.objects.filter(country=c)
    rounds = Round.objects.filter(game=game)
    orders = []
    for round_ in rounds:
        orders.append(Order.objects.filter(country=c,round=round_).order_by("-pub_date").first())
    return render(request, 'wd/country.html', {
        'game': game,
        'rounds':rounds,
        'c':c,
        'orders':orders,
        'cities':cities,
    })


def reset(request,game_id):
    if(request.user.id!=1):
        return redirect("wd:game",game_id)
    game = Game.objects.filter(id=game_id).first()
    c=Country.objects.filter(game=game)
    for country in c:
        cities = City.objects.filter(country=country)
        country.budget = 1000
        country.technology = False
        country.rockets = 0
        i = 0
        for city in cities:
            city.shield = False
            if(i == 0):
                city.status = 100
            elif(i==1):
                city.status = 80
            elif(i==2):
                city.status = 60
            else:
                city.status = 40
            i+=1
            city.save(update_fields=["shield","status"])
        country.save(update_fields=["technology","rockets","budget"])
    return redirect("wd:orders",game_id)
        


    



def chat_room(request, label):
    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    room, created = Room.objects.get_or_create(label=label)

    # We want to show the last 50 messages, ordered most-recent-last
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    return render(request, "wd/room.html", {
        'room': room,
        'messages': messages,
    })



# @login_required(login_url='/login/')
# def user_list(request):
#     """
#     NOTE: This is fine for demonstration purposes, but this should be
#     refactored before we deploy this app to production.
#     Imagine how 100,000 users logging in and out of our app would affect
#     the performance of this code!
#     """
#     users = User.objects.select_related('logged_in_user')
#     for user in users:
#         user.status = 'Online' if hasattr(user, 'logged_in_user') else 'Offline'
#     return render(request, 'wd/user_list.html', {'users': users})
