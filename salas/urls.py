from django.urls import path
from .views import SalaListView, QuartoCreateView, SalaComercialCreateView, SalaDeleteView, \
    QuartoUpdateView, SalaComercialUpdateView

urlpatterns = [
    path('', SalaListView.as_view(), name='salas'),
    path('adicionar/quarto/', QuartoCreateView.as_view(), name='quarto_adicionar'),
    path('adicionar/comercial/', SalaComercialCreateView.as_view(), name='sala_comercial_adicionar'),
    path('<int:pk>/editar/quarto/', QuartoUpdateView.as_view(), name='quarto_editar'),
    path('<int:pk>/editar/comercial/', SalaComercialUpdateView.as_view(), name='sala_comercial_editar'),
    path('<int:pk>/apagar/', SalaDeleteView.as_view(), name='sala_apagar'),
]