from django.urls import path
from .views import ChaveListView, ChaveCreateView, ChaveUpdateView, ChaveDeleteView

urlpatterns = [

    path('', ChaveListView.as_view(), name='chaves'),
    path('adicionar/', ChaveCreateView.as_view(), name='chave_adicionar'),
    path('<int:pk>/editar/', ChaveUpdateView.as_view(), name='chave_editar'),
    path('<int:pk>/apagar/', ChaveDeleteView.as_view(), name='chave_apagar'),
]