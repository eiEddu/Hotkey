from django.urls import path

from reservas.views import ReservaListView, ReservaCreateView, ReservaUpdateView, ReservaDeleteView

urlpatterns = [
    path('',ReservaListView.as_view(),name='reservas'),
    path('adicionar/',ReservaCreateView.as_view(),name='reserva_adicionar'),
    path('<int:pk>/editar/',ReservaUpdateView.as_view(),name='reserva_editar'),
    path('<int:pk>/apagar/',ReservaDeleteView.as_view(),name='reserva_apagar'),
]