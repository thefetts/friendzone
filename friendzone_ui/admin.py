from django.contrib import admin

from .models.friend import Friend
from .models.friendship import Friendship

admin.site.register(Friend)
admin.site.register(Friendship)
