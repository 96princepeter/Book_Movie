from .views import *
from django.urls import path
from . import views
from project_movie.settings import DEBUG, STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from django.conf.urls import include,re_path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('rating',RatingView)
router.register('movie',MovieView)


#Registration and login urls

urlpatterns = [
    path('', home, name = 'homepage'),
    path('about/', about, name = 'about'),
    path('registration/', registration, name='registration'),
]


# Movie related urls

urlpatterns += [
    path('library/', views.index, name = 'index'),
    path('user/', LocationUpdate.as_view(), name = 'user_location'),
    path('upload/', views.upload, name = 'upload-Movie'),

    path('location/', Location.as_view(), name = 'upload-Location'),
    path('location/running/<int:movie_id>', UpdateLocation.as_view(), name = 'add-Location'),

    path('library/update/<int:movie_id>', views.update_Movie),
    path('library/delete/<int:movie_id>', views.delete_Movie),
    path('library/about_view/<int:movie_id>',views.about_view),

    path('library/rating/<int:movie_id>',RateView.as_view()),
    path('',include(router.urls)),
    path('chat/', views.chatindex, name='chat'),
    path('chat/<str:room_name>/', views.room, name='room'),
]
#DataFlair
if DEBUG:
    urlpatterns += static(STATIC_URL, document_root = STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root = MEDIA_ROOT)