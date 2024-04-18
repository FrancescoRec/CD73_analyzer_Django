from django.urls import path
from . import views

urlpatterns = [
    path('predict_molecule/', views.predict_molecule, name='predict_molecule'),
    path('download/',  views.download_view, name='download_view'),
]
