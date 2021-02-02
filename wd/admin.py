from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

class PlayerAdmin(UserAdmin):
    # autocomplete_fields=["school_id"]
    list_display = ('username','last_login','date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser','last_login','date_joined')
        })
    )
    # inlines = [CourseInline,]

admin.site.register(Player,PlayerAdmin)
admin.site.register(Game)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Order)
admin.site.register(Round)
admin.site.register(Timer)
