from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.say_hello) # first argument is the URL pattern (the end), second argument is the view function
    
]

