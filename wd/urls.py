"""ugolok URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from wd import views
import requests
from django.conf.urls.static import static
from ugolok import settings
from ugolok import views as uviews
# from wd import url

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('main', views.index, name='index'),
    # path('', uviews.index, name='index'),
    # path('u/', views.user_list, name='user_list'),
    # path('game/', views.enter, name='game'),
    # path('<str:room_name>/', views.room, name='room'),
    path('lobby/<int:game_id>/', views.lobby, name='lobby'),
    path('game/<int:game_id>/', views.game, name='game'),
    path('game/<int:game_id>/order/', views.order, name='order'),
    path('game/<int:game_id>/country/', views.country, name='country'),
    path('game/<int:game_id>/orders/', views.orders, name='orders'),
    path('game/<int:game_id>/orders/apply/<int:round_id>/', views.apply_round, name='round_apply'),
    path('lobby/create/', views.creategame, name='create'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(r'^favicon.ico$', document_root='media/logo/favicon.ico')
