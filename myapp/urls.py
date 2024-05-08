from django.urls import path
from . import views
urlpatterns = [
    path('', views.base, name='base'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('enter-results/', views.enter_results, name='enter_results'),
    path('workout-program/', views.workout_program, name='workout_program'),
    
]
