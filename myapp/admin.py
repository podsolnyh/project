from django.contrib import admin
from .models import ExerciseRating
from .models import Exercise
from .models import AgeGroup, Gender
from .models import Profile
from django.forms import Textarea
from django.db import models
from .models import Profile



class ExerciseRatingAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'age_group', 'gender', 'score_1', 'score_2', 'score_3', 'score_4', 'score_5')
    search_fields = ('exercise__name', 'age_group__name', 'gender__name')
    
class ProfileAdmin(admin.ModelAdmin):
    # Определение полей для поиска
    search_fields = ['user__username']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Exercise)
admin.site.register(ExerciseRating, ExerciseRatingAdmin)
admin.site.register(AgeGroup)
admin.site.register(Gender)




