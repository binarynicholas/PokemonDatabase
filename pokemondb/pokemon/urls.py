from django.urls import path

from . import views

app_name = 'pokemondb'
urlpatterns = [
    path('', views.SpeciesList.as_view(), name='index'),
    path('<int:pk>/', views.SpeciesView.as_view(), name='species_detail'),
    path('ability/<int:pk>/', views.AbilityView.as_view(), name='ability_detail'),
    path('move/<int:pk>/', views.MoveView.as_view(), name='move_detail'),
    path('api/moves/', views.ScrapeMoves.as_view(), name='get_api_moves')
]