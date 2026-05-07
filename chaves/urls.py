from django.urls import path
from .views import ChaveListView, ChaveBlocoCreateView,ChaveQuartoCreateView,ChaveSalaComercialCreateView,ChaveUpdateView,ChaveDeleteView

urlpatterns = [
    path('', ChaveListView.as_view(), name='chaves'),
    path('adicionar/bloco/', ChaveBlocoCreateView.as_view(), name='chave_bloco_adicionar'),
    path('adicionar/quarto/', ChaveQuartoCreateView.as_view(), name='chave_quarto_adicionar'),
    path('adicionar/sala-comercial/', ChaveSalaComercialCreateView.as_view(), name='chave_sala_comercial_adicionar'),
    path('<int:pk>/editar/', ChaveUpdateView.as_view(), name='chave_editar'),
    path('<int:pk>/apagar/', ChaveDeleteView.as_view(), name='chave_apagar'),
]