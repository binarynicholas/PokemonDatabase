from django.urls import path

from . import views

app_name = 'pokemondb'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pokemon_id>/', views.speciesDetails, name='speciesDetails'),
    path('ability/<int:ability_id>/', views.abilityDetails, name='abilityDetails'),
]