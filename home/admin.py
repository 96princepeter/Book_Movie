from django.contrib import admin
from .models import Movie,UsersLocation,Rating,MovieLocation,Locations
# Register your models here.
admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(UsersLocation)
admin.site.register(MovieLocation)
admin.site.register(Locations)