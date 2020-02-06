from django.contrib import admin
from .models import Movie,Location,Rating
# Register your models here.
admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Location)