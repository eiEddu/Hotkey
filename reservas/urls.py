from django.urls import path
from .views import ReservaListView, ReservaQuartoCreateView, ReservaSalaComercialCreateView, \
    ReservaDeleteView, ReservaSalaComercialUpdateView, ReservaQuartoUpdateView

urlpatterns = [
    path('', ReservaListView.as_view(), name='reservas'),
    path('adicionar/quarto/', ReservaQuartoCreateView.as_view(), name='reserva_quarto_adicionar'),
    path('adicionar/sala-comercial/', ReservaSalaComercialCreateView.as_view(), name='reserva_sala_comercial_adicionar'),
    path('<int:pk>/editar/quarto/', ReservaQuartoUpdateView.as_view(), name='reserva_quarto_editar'),
    path('<int:pk>/editar/sala-comercial/', ReservaSalaComercialUpdateView.as_view(), name='reserva_sala_comercial_editar'),
    path('<int:pk>/apagar/', ReservaDeleteView.as_view(), name='reserva_apagar'),
]