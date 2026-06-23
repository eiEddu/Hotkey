from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from funcionarios.forms import FuncionarioModelForm
from funcionarios.models import Funcionario


class FuncionarioListView(PermissionRequiredMixin,ListView):
    permission_required = 'funcionarios.view_funcionario'
    permission_denied_message = 'Visualizar funcionário'
    model = Funcionario
    template_name = 'funcionarios.html'

    def get_queryset(self):
        qs = super(FuncionarioListView, self).get_queryset()
        nome = self.request.GET.get('nome')
        cpf = self.request.GET.get('cpf')
        cargo = self.request.GET.get('cargo')

        if nome:
            qs = qs.filter(nome__icontains=nome)
        if cpf:
            qs = qs.filter(cpf__icontains=cpf)
        if cargo:
            qs = qs.filter(cargo=cargo)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhum funcionário encontrado com estes filtros!')

class FuncionarioCreateView(PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'funcionarios.add_funcionario'
    permission_denied_message = 'Cadastrar funcionário'
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy ('funcionarios')
    success_message = 'Funcionário cadastrado com sucesso!'

class FuncionarioUpdateView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'funcionarios.update_funcionario'
    permission_denied_message = 'Atualizar funcionário'
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy ('funcionarios')
    success_message = 'Funcionário atualizado com sucesso!'

class FuncionarioDeleteView(PermissionRequiredMixin,SuccessMessageMixin, DeleteView):
    permission_required = 'funcionarios.delete_funcionario'
    permission_denied_message = 'Deletar funcionario'
    model = Funcionario
    template_name = 'funcionario_apagar.html'
    success_url = reverse_lazy ('funcionarios')
    success_message = 'Funcionario apagado com sucesso!'