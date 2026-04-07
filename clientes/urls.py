from django.urls import path
from .views import ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView

urlpatterns = [

    path('', ClienteListView.as_view(), name='clientes'),
    path('adicionar/', ClienteCreateView.as_view(), name='cliente_adicionar'),
    path('<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente_editar'),
    path('<int:pk>/apagar/', ClienteDeleteView.as_view(), name='cliente_apagar'),
]