from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default='avatar.svg')

    balance = models.DecimalField(max_digits=20, decimal_places=2, null=False, default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class UserLikes(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class UserFlags(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agreeableness = models.IntegerField(null=True, default=0)
    conscientiousness = models.IntegerField(null=True, default=0)
    extraversion = models.IntegerField(null=True, default=0)
    openness = models.IntegerField(null=True, default=0)
    emotional_stability = models.IntegerField(null=True, default=0)
        
    likes = models.ManyToManyField(UserLikes)

    interest_economic = models.IntegerField(null=True, default=0)
    interest_social = models.IntegerField(null=True, default=0)
    interest_spiritual = models.IntegerField(null=True, default=0)
    interest_political = models.IntegerField(null=True, default=0)

    sex = models.IntegerField(null=True, default=0) 
    age = models.IntegerField(null=True, default=0) 
    flags = models.ManyToManyField(UserFlags)
    profession = models.CharField(max_length=200)
    social_level = models.IntegerField(null=True, default=0) 
    education = models.CharField(max_length=200)


class Train(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class TransactionKarma(models.Model):
    name = models.CharField(max_length=200, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, null=False, default=0)
    addition = models.BooleanField(null=False, default=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
class RoomStatus(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    train = models.ForeignKey(Train, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(RoomStatus, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-updated', '-created']

class MatchType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Match(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    type = models.ForeignKey(MatchType, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-created']

class ReviewType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Review(models.Model):
    rating = models.SmallIntegerField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    type = models.ForeignKey(ReviewType, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-created']

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField() 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
