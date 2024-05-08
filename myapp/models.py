
from django.db import models
from django.contrib.auth.models import User
import json
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.user.username
   
class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    exercise_ratings = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username}'
    
    


class AgeGroup(models.Model):
    min_age = models.IntegerField(verbose_name='Минимальный возраст',default=6)
    max_age = models.IntegerField(verbose_name='Максимальный возраст',default=100)

    def __str__(self):
        return f'{self.min_age} - {self.max_age} лет'


class Gender(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'

class Exercise(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

class ExerciseRating(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    score_1 = models.FloatField(default=0)
    score_2 = models.FloatField(default=0)
    score_3 = models.FloatField(default=0)
    score_4 = models.FloatField(default=0)
    score_5 = models.FloatField(default=0)
    score_6 = models.FloatField(default=0)
    score_7 = models.FloatField(default=0)
    score_8 = models.FloatField(default=0)
    score_9 = models.FloatField(default=0)
    score_10 = models.FloatField(default=0)
   

