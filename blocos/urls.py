from django.urls import path

from blocos.views import BlocoListView, BlocoUpdateView, BlocoDeleteView, BlocoCreateView

urlpatterns = [
    path('',BlocoListView.as_view(),name='blocos'),
    path('adicionar/',BlocoCreateView.as_view(),name='bloco_adicionar'),
    path('<int:pk>/editar/',BlocoUpdateView.as_view(),name='bloco_editar'),
    path('<int:pk>/apagar/',BlocoDeleteView.as_view(),name='bloco_apagar'),
]