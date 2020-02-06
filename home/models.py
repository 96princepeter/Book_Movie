from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator


class Location(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    location = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % (self.location)

class Movie(models.Model):
    name = models.CharField(max_length=50)
    picture = models.ImageField()
    director = models.CharField(max_length=30, default='Director Name')
    describe = models.TextField(default='Something Related Movie')
    location = models.CharField(max_length=50, null=True)
    def no_of_rating(self):
        rating = Rating.objects.filter(movie=self)
        return len(rating)
    def avg_rating(self):
        sum=0
        rating = Rating.objects.filter(movie=self)
        for ratings in rating:
            sum+=ratings.star
        if len(rating)>0:
            return sum/len(rating)
        else:
            return 0


class Rating(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    star = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    class Meta:
        unique_together = (('user','movie'),)
        index_together = (('user','movie'),)