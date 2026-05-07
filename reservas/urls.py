from django.urls import path
from .views import ReservaListView, ReservaQuartoCreateView, ReservaSalaComercialCreateView, ReservaUpdateView, ReservaDeleteView

urlpatterns = [
    path('', ReservaListView.as_view(), name='reservas'),
    path('adicionar/quarto/', ReservaQuartoCreateView.as_view(), name='reserva_quarto_adicionar'),
    path('adicionar/sala-comercial/', ReservaSalaComercialCreateView.as_view(), name='reserva_sala_comercial_adicionar'),
    path('<int:pk>/editar/', ReservaUpdateView.as_view(), name='reserva_editar'),
    path('<int:pk>/apagar/', ReservaDeleteView.as_view(), name='reserva_apagar'),
]