from django.contrib import admin
from .models import Film, ExtraInfo, Review, Actor

admin.site.register(Film)
admin.site.register(ExtraInfo)
admin.site.register(Review)
admin.site.register(Actor)