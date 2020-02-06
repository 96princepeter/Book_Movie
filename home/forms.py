from django import forms
from .models import Movie
from .models import Location
#DataFlair
class MovieCreate(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

class MovieSearch(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
