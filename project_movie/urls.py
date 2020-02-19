
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.views.generic.base import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('user/', include('django.contrib.auth.urls')),

]
