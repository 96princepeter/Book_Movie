from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
import datetime
from django.views.generic.base import TemplateView
from .models import Movie, UsersLocation, Rating, MovieLocation, Locations
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

"""
    
    AFATER LOGIN
    
        
"""
#login function required templatres
@login_required(login_url='homepage')
def index(request): #index
    if request.user.is_staff:
        shelf = Movie.objects.all()
        return render(request, 'movie/library.html', {'shelf': shelf})
    else:

        location = UsersLocation.objects.filter(user=request.user)
        if location.exists():
            movies = MovieLocation.objects.filter(location= location.first().location)
        else:
            movies = ''
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



#class adding and update movie location
class Location(TemplateView):
    template_name = 'movie/movie_location.html'
    def get(self, request, *args, **kwargs):
        shelf = Movie.objects.all()
        return render(request, self.template_name, {'shelf': shelf})


#adding new movie location
class UpdateLocation(TemplateView):
    template_name = 'movie/update_location.html'

    def get(self, request, *args, **kwargs):
        movie_id = self.kwargs.get('movie_id', None)
        if movie_id:
            movies = Movie.objects.get(id=movie_id)
        movie_loc_qs = MovieLocation.objects.filter(movie_id=movie_id)
        locations = Locations.objects.all()
        return render(request, self.template_name, {'shelf': movies, 'data': movie_loc_qs, 'locations': locations})

    def post(self,request,  *args, **kwargs):
        loc_id = request.POST.get('location_select')
        movie_id = self.kwargs.get('movie_id', None)
        MovieLocation.objects.get_or_create(location_id=loc_id, movie_id=movie_id)
        movies = Movie.objects.get(id=movie_id)
        locations = Locations.objects.all()
        movie_loc_qs = MovieLocation.objects.filter(movie_id=movie_id)
        print(movie_loc_qs )
        return render(request, self.template_name, {'shelf': movies, 'data': movie_loc_qs, 'locations': locations})
        # return redirect('upload-Location')

# adding locations to each movies running by functions
def upload(request):
    upload = MovieCreate()
    if request.method == 'POST':
        upload = MovieCreate(request.POST, request.FILES)
        if upload.is_valid():
            print(upload)

            upload.save()
            return redirect('index')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'movie/upload_form.html', {'upload_form':upload})


#class by user location adding and update
class LocationUpdate(TemplateView):
    template_name = 'user/location_update.html'

    def get(self, request, *args, **kwargs):
        location = UsersLocation.objects.filter(user=request.user)
        location_all = Locations.objects.all()
        if location:
            return render(request,self.template_name,{'location': location.first(), 'location_all': location_all})
        else:
            return render(request,self.template_name,{'location_all': location_all})

    def post(self, request):
        location = request.POST.get('loc')
        user = request.user
        user_loc = UsersLocation.objects.filter(user=user)

        if user_loc:
            location_qs = UsersLocation.objects.filter(user=user)
            location_qs.update(location=location)
        else:
             loc = Locations.objects.filter(id=location)
             print(loc.first())
             UsersLocation.objects.create(user=user,location=loc.first())
            # print('check end ')
        return redirect('index')


#Rattinng movies

class RateView(TemplateView):
    def get(self, request, *args, **kwargs):
        movie_id = self.kwargs.get('movie_id', None)
        print(movie_id)
        movie_sel,obj = Rating.objects.get_or_create(movie_id=movie_id,user=request.user)

        return render(request, 'user/rating.html', {'rating': movie_sel})

    def post(self, request, *args, **kwargs):
        movie_id = kwargs.get('movie_id', None)
        new_rate = request.POST.get('rating')
        Rating.objects.filter(movie_id=movie_id).update(star=new_rate)
        movie_sel = Rating.objects.get(movie_id=movie_id)
        return render(request, 'user/rating.html', {'rating': movie_sel})





#serializers class
class RatingView(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class MovieView(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


#chatting



def chatindex(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })