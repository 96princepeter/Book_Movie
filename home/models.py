from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save



"""
 Movie, Movie Location , User Location Rating are  in the Models 
 and Movie are the basic parent model  
"""
#Movie model
class Locations(models.Model):
    location_name = models.CharField(max_length=30, null=True)
    def __str__(self):
        return '%s' % (self.location_name)

#movie details

class Movie(models.Model):
    name = models.CharField(max_length=50)
    picture = models.ImageField()
    director = models.CharField(max_length=30, default='Director Name')
    describe = models.TextField(default='Something Related Movie')
    status = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(2)], default=0,null=False)
    location = models.ManyToManyField(Locations)
    def no_of_rating(self): #the dunction calculated the total number of rating
        rating = Rating.objects.filter(movie=self)
        return len(rating)
    def avg_rating(self):  #the function calculate the average value of rating in very time
        sum=0
        rating = Rating.objects.filter(movie=self)
        for ratings in rating:
            sum+=ratings.star
        if len(rating)>0:
            return sum/len(rating)
        else:
            return 0

    def __str__(self):
        return '%s' % self.name





class UsersLocation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    location = models.ForeignKey(Locations,on_delete=models.CASCADE)
    class Meta:
        unique_together = (('user', 'location'),)

    def __str__(self):
        return '%s' % (self.location)

# #movie location model
# class MovieLocation(models.Model):
#     movie=models.ManyToManyField(Movie)
#     location = models.ManyToManyField(Locations)
#
#     def __str__(self):
#         return '%s - %s' % (self.movie, self.location)


class Rating(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    star = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)], default=0 ,null=True)
    # class Meta:
    #     unique_together = (('user','movie'),)
    #     index_together = (('user','movie'),)

    def __str__(self):
        return '%s - %s' % (self.movie, self.star)




class Chat(models.Model):
    room_name = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.room_name.username

def create_room(sender,**kwargs):
    if kwargs['created']:
        chat = Chat.objects.create(room_name=kwargs['instance'])
post_save.connect(create_room,sender=User)



class Messages(models.Model):
    room = models.ForeignKey(Chat,related_name='chatroom',on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField(max_length=230)
    timestamp = models.DateTimeField(auto_now_add=True)

