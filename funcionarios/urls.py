from django.urls import path

from funcionarios.views import FuncionarioListView, FuncionarioDeleteView, FuncionarioUpdateView, FuncionarioCreateView

urlpatterns = [

    path('', FuncionarioListView.as_view(), name='funcionarios'),
    path('adicionar/', FuncionarioCreateView.as_view(), name='funcionario_adicionar'),
    path('<int:pk>/editar/', FuncionarioUpdateView.as_view(), name='funcionario_editar'),
    path('<int:pk>/apagar/', FuncionarioDeleteView.as_view(), name='funcionario_apagar'),
]