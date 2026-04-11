from django.urls import path
from .views import SalaUpdateView,SalaDeleteView,SalaCreateView,SalaListView

urlpatterns = [

    path('', SalaListView.as_view(), name='salas'),
    path('adicionar/', SalaCreateView.as_view(), name='sala_adicionar'),
    path('<int:pk>/editar/', SalaUpdateView.as_view(), name='sala_editar'),
    path('<int:pk>/apagar/', SalaDeleteView.as_view(), name='sala_apagar'),
]