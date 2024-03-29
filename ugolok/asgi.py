"""
ASGI config for ugolok project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""
# mysite/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import wd.routing
# from channels.auth import channel_session_user_from_http
# from channels import Group

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ugolok.settings')


application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            wd.routing.websocket_urlpatterns
        )
    ),
})