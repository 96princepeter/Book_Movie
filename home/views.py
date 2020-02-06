from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
import datetime
from django.views.generic.base import TemplateView
from .models import Movie,Location,Rating
from .forms import MovieCreate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import RatingSerializer,MovieSerializer

"""
  Base, Registration and About templates
"""

def home(request):
    return render(request, 'home.html')

def registration(request):
    """
    registration function
    :param request: User Registration
    :return:
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})
def about(request):
    time = datetime.datetime.now()
    return render(request, 'about.html', {'time': time})


#login function required templatres
@login_required(login_url='homepage')

#Index page
def index(request):
    if request.user.is_staff:
        shelf = Movie.objects.all()
        return render(request, 'movie/library.html', {'shelf': shelf})
    else:
        location = Location.objects.get(user=request.user)
        movies=  Movie.objects.filter(location= location)
        return render(request, 'movie/library.html', {'movies': movies})



@login_required(login_url='homepage')
#upload movie page
def upload(request):
    upload = MovieCreate()
    if request.method == 'POST':
        upload = MovieCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('index')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'movie/upload_form.html', {'upload_form':upload})

@login_required(login_url='homepage')
#update page
def update_Movie(request, movie_id):
    movie_id = int(movie_id)
    try:
        movie_sel = Movie.objects.get(id = movie_id)
    except Movie.DoesNotExist:
        return redirect('index')

    movie_form = MovieCreate(request.POST or None, instance = movie_sel)
    if movie_form.is_valid():
       movie_form.save()
       return redirect('index')
    return render(request, 'movie/upload_form.html', {'upload_form':movie_form})

@login_required(login_url='homepage')
#delete Movies page
def delete_Movie(request, movie_id):
    movie_id = int(movie_id)
    try:
        movie_sel = Movie.objects.get(id = movie_id)
    except Movie.DoesNotExist:
        return redirect('index')
    movie_sel.delete()
    return redirect('index')

@login_required(login_url='homepage')
#about view page
def about_view(request, movie_id):
    movie_id = int(movie_id)
    try:
        movie_sel = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return redirect('index')
    return render(request, 'movie/about.html', {'about':movie_sel})
    return redirect('index')

#Rattinng movies
def rateview(request,movie_id):
    movie_id = int(movie_id)
    try:
        movie_sel = Rating.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return redirect('index')
    return render(request, 'user/rating.html', {'rating': movie_sel})


#class by location adding and update
class LocationUpdate(TemplateView):
    template_name = 'user/location_update.html'

    def get(self, request, *args, **kwargs):
        location = Location.objects.filter(user=request.user)
        if location:
            return render(request,self.template_name,{'location': location.first()})
        else:
            return render(request,self.template_name,{})

    def post(self, request):
        location = request.POST.get('location')
        location_qs = Location.objects.filter(user=request.user)
        location_qs.update(location=location)
        return render(request, 'movie/library.html', {'location': location_qs.first()})


#serializers class
class RatingView(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class MovieView(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer