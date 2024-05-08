from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import ExerciseRating
from django.core.exceptions import ValidationError

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''  # Убираем стандартные подсказки для всех полей
           

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'age']

class ResultsForm(forms.Form):
    long_jump = forms.IntegerField(label='Прыжок в длину с места (см)')
    def clean_long_jump(self):
        data = self.cleaned_data['long_jump']
        if data < 0:
            raise ValidationError("Прыжок в длину не может быть отрицательным")
        return data
    
    forward_bend = forms.IntegerField(label='Наклон вперед из положения сидя (см)')

    push_ups = forms.IntegerField(label='Сгибание и разгибание рук в упоре лежа, раз')
    def clean_push_ups(self):
        data = self.cleaned_data['push_ups']
        if data < 0:
            raise ValidationError("Сгибание и разгибание рук в упоре лежа не может быть отрицательным значением")
        return data
    
    pull_ups = forms.IntegerField(label='Подтягивания на высокой перекладине, раз')
    def clean_pull_ups(self):
        data = self.cleaned_data['pull_ups']
        if data < 0:
            raise ValidationError("Подтягивания на высокой перекладине не могут быть отрицательными значениями")
        return data
    
    sit_ups = forms.IntegerField(label='Поднимание туловища из положения лежа на спине (за 60 с), раз')
    def clean_sit_ups(self):
        data = self.cleaned_data['sit_ups']
        if data < 0:
            raise ValidationError("Поднимание туловища из положения лежа на спине (за 60 с) не может быть отрицательным значением")
        return data
    
    shuttle_run = forms.FloatField(label='Челночный бег 4x9 м (с)')
    def clean_shuttle_run(self):
        data = self.cleaned_data['shuttle_run']
        if data < 0:
            raise ValidationError("Время не может быть отрицательным")
        return data
    
    sprint_30m = forms.FloatField(label='Бег 30 м (с)')
    def clean_sprint_30m(self):
        data = self.cleaned_data['sprint_30m']
        if data < 0:
            raise ValidationError("Время не может быть отрицательным")
        return data
    
    run_3000m = forms.FloatField(label='Бег 3000 м (мин)')
    def clean_run_3000m(self):
        data = self.cleaned_data['run_3000m']
        if data < 0:
            raise ValidationError("Время не может быть отрицательным")
        return data
    
class ExerciseRatingForm(forms.ModelForm):
    class Meta:
        model = ExerciseRating
        fields = '__all__'
    