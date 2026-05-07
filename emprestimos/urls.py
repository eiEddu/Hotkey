from django.urls import path
from .views import (
    EmprestimoListView,
    EmprestimoQuartoCreateView,
    EmprestimoSalaComercialCreateView,
    EmprestimoDeleteView,
    EmprestimoDevolucaoView
)

urlpatterns = [
    path('', EmprestimoListView.as_view(), name='emprestimos'),
    path('adicionar/quarto/', EmprestimoQuartoCreateView.as_view(), name='emprestimo_quarto_adicionar'),
    path('adicionar/comercial/', EmprestimoSalaComercialCreateView.as_view(), name='emprestimo_comercial_adicionar'),
    path('<int:pk>/apagar/', EmprestimoDeleteView.as_view(), name='emprestimo_apagar'),
    path('<int:pk>/devolver/', EmprestimoDevolucaoView.as_view(), name='emprestimo_devolver'),
]