from django.contrib import admin
from .models import (
    Movie,
    UsersLocation,
    Rating,
    Locations,
    Chat,
    Messages,
)
# Register your models here.
admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(UsersLocation)
admin.site.register(Locations)
admin.site.register(Chat)
admin.site.register(Messages)