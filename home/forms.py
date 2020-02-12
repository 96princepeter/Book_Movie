from django import forms
from .models import Movie,MovieLocation
from .models import UsersLocation,Rating
#DataFlair
class MovieCreate(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

class MovieSearch(forms.ModelForm):
    class Meta:
        model = UsersLocation
        fields = '__all__'

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = '__all__'

class MovieLocationForm(forms.ModelForm):
    class Meta:
        model = MovieLocation
        fields = '__all__'
