from django.urls import path
from .views import ChaveListView, ChaveBlocoCreateView, ChaveQuartoCreateView, ChaveSalaComercialCreateView, ChaveDeleteView, ChaveBlocoUpdateView

urlpatterns = [
    path('', ChaveListView.as_view(), name='chaves'),
    path('adicionar/bloco/', ChaveBlocoCreateView.as_view(), name='chave_bloco_adicionar'),
    path('adicionar/quarto/', ChaveQuartoCreateView.as_view(), name='chave_quarto_adicionar'),
    path('adicionar/sala-comercial/', ChaveSalaComercialCreateView.as_view(), name='chave_sala_comercial_adicionar'),
    path('<int:pk>/editar/bloco/', ChaveBlocoUpdateView.as_view(), name='chave_bloco_editar'),
    path('<int:pk>/editar/quarto/', ChaveQuartoCreateView.as_view(), name='chave_quarto_editar'),
    path('<int:pk>/editar/sala-comercial/', ChaveSalaComercialCreateView.as_view(), name='chave_sala_comercial_editar'),
    path('<int:pk>/apagar/', ChaveDeleteView.as_view(), name='chave_apagar'),
]