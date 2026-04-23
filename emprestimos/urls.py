from django.urls import path

from emprestimos.views import EmprestimoListView, EmprestimoCreateView, EmprestimoUpdateView, EmprestimoDeleteView

urlpatterns = [
    path('',EmprestimoListView.as_view(),name='emprestimos'),
    path('adicionar/',EmprestimoCreateView.as_view(),name='emprestimo_adicionar'),
    path('<int:pk>/editar/',EmprestimoUpdateView.as_view(),name='emprestimo_editar'),
    path('<int:pk>/apagar/',EmprestimoDeleteView.as_view(),name='emprestimo_apagar'),
]