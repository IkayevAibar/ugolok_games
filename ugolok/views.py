
from django.shortcuts import render,redirect
from django.urls import reverse
from datetime import datetime
from wd.models import *
import requests
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

# Create your views here.
def index(request):
    return render(request,template_name='ugolok/index.html')

class PlayerCreationForm(UserCreationForm):
    class Meta:
        model=Player 
        fields = ('username', 'password1', 'password2')


def sign_up(request):
    form = PlayerCreationForm()
    if request.method == 'POST':
        form = PlayerCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
        else:
            print(form.errors)
    return render(request, 'ugolok/sign_up.html', {'form': form})