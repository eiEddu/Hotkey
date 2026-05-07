from django.urls import path
from .views import SalaListView, QuartoCreateView, SalaComercialCreateView, SalaUpdateView, SalaDeleteView


urlpatterns = [
    path('', SalaListView.as_view(), name='salas'),
    path('adicionar/quarto/', QuartoCreateView.as_view(), name='quarto_adicionar'),
    path('adicionar/comercial/', SalaComercialCreateView.as_view(), name='sala_comercial_adicionar'),
    path('<int:pk>/editar/', SalaUpdateView.as_view(), name='sala_editar'),
    path('<int:pk>/apagar/', SalaDeleteView.as_view(), name='sala_apagar'),
]