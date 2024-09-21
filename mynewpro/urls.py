# In urls.py
from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include  # Add 'include' here
from .views import AuthView,AdminView,user_list_view,home,profile,about,caretaker,book_caretaker
urlpatterns = [
    
    path('', AuthView.as_view(), name='auth'),
     path('auth/', AuthView.as_view(), name='auth'), 
    path('users_list/', user_list_view, name='users_list'),
    #   path('auth/', AuthView.as_view(), name='auth'),  # Auth view for login/signup
    path('admin/', AdminView.as_view(), name='admin'),  # Admin view
     path('home/', home, name='home'),
     path('profile/',profile, name='profile'),
     
    #path('profile/<str:user_id>/', profile_view, name='profile'),
    #path('book/<str:user_id>/', book_caretaker, name='book_caretaker'), 
     path('caretaker/',caretaker, name='caretaker'),
     path('aboutus/',about, name='aboutus'),
     
]

