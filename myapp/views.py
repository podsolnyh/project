from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate,logout
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import  Profile  
from .forms import ProfileForm
from django.shortcuts import render, get_object_or_404
from .forms import ResultsForm
from .forms import ExerciseRating
from django.shortcuts import redirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django import forms
def base(request):
    return render(request, 'base.html')
def home(request):
    return render(request, 'home.html')


    
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем нового пользователя в базе данных
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            Profile.objects.create(user=user)
            login(request, user)  # Аутентификация пользователя после регистрации
            return redirect('home')  # Перенаправляем на домашнюю страницу
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        Profile.objects.create(user=instance, age=20, gender='M')  # Здесь установите значения по умолчанию

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_superuser:
        instance.profile.save()

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('base')

@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})

def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Перенаправление на страницу профиля после сохранения
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form})



def enter_results(request):
    user_profile = Profile.objects.filter(user=request.user).first()
    if not user_profile or not user_profile.age or not user_profile.gender:
        # Если профиль не найден или не заполнены возраст или пол
        message = 'Заполните свой профиль (укажите возраст и пол)!'
        return render(request, 'enter_results.html', {'message': message})
    if request.method == 'POST':
        form = ResultsForm(request.POST)
        if form.is_valid():
            exercise_ratings = {}
            exercise_grade = None
            age = user_profile.age
            gender = user_profile.gender  # Пол пользователя (например, 'M' или 'F')
            
            exercises = [
                ('long_jump', 'Прыжок в длину'),
                ('forward_bend', 'Наклон вперед из положения сидя'),
                ('push_ups' ,'Сгибание и разгибание рук в упоре лежа'),
                ('pull_ups' ,'Подтягивания на высокой перекладине'),
                ('sit_ups' ,'Поднимание туловища из положения лежа на спине'),
                ('shuttle_run' ,'Челночный бег 4x9'),
                ('sprint_30m' ,'Бег 30 м'),
                ('run_3000m' ,'Бег 3000 м'),
            ]
            
            # Нахождение соответствующей записи ExerciseRating на основе возраста и пола
            for exercise_field, exercise_label in exercises:
                exercise_result = request.POST.get(exercise_field, 0)
                try:
                    exercise_rating = ExerciseRating.objects.get(
                        age_group__min_age__lte=age,
                        age_group__max_age__gte=age,
                        gender__name=gender,
                        exercise__name=exercise_field
                    )

                    # Теперь у нас есть нужная запись ExerciseRating для использования
                    # Продолжим обработку результатов и отображение оценки
                    exercise_result = float(request.POST.get(exercise_field, 0))

                    # Получение оценки на основе результата упражнения
                    if exercise_field in ["shuttle_run", "sprint_30m", "run_3000m"]:
                    #  логика для упражнений с временными результатами
                        for i in range(1, 11):
                            score_lower = getattr(exercise_rating, f"score_{i}")
                            if i < 10:
                                score_upper = getattr(exercise_rating, f"score_{i+1}")
                                if score_lower > exercise_result >= score_upper:
                                    exercise_grade = i
                                    break
                                if exercise_result > score_lower:
                                    exercise_grade = 1
                                    break
                            else:
                                if score_lower >= exercise_result:
                                    exercise_grade = i
                                    break
                            
                    else:
                        for i in range(1, 11):
                            score_lower = getattr(exercise_rating, f"score_{i}")
                            if i < 10:
                                score_upper = getattr(exercise_rating, f"score_{i+1}")
                                if score_lower < exercise_result <= score_upper:
                                    exercise_grade = i
                                    break
                            else:
                                # Последний диапазон (score_10 и выше)
                                if score_lower <= exercise_result:
                                    exercise_grade = i
                                    break
                        
                    if exercise_grade is None:
                        # В случае, если результат не попадает ни в один из диапазонов
                        exercise_grade = 1  # Минимальная оценка
                    
                    # Другие условия для определения оценки
                    exercise_ratings[exercise_label] = exercise_grade

                except ExerciseRating.DoesNotExist:
                    # Обработка случая, если не найдено соответствующей записи ExerciseRating
                    pass
                
            context = {
                'form': form,
                'exercise_ratings': exercise_ratings
            }
            user_profile.exercise_ratings = exercise_ratings
            user_profile.save()
            return render(request, 'enter_results.html', context)
                
    else:
        form = ResultsForm()
        if user_profile.gender == 'F':  # Проверяем, если пол женский
                # Скрываем поле "Подтягивания на высокой перекладине" для женщин
                form.fields['pull_ups'].widget = forms.HiddenInput()
    return render(request, 'enter_results.html', {'form': form})

def workout_program(request):
    return render(request, 'workout_program.html')


