from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Cliente
from .forms import ClienteModelForm


class ClienteListView(PermissionRequiredMixin,ListView):
    permission_required = 'clientes.view_cliente'
    permission_denied_message = 'Visualizar cliente'
    model = Cliente
    template_name = 'clientes.html'

    def get_queryset(self):
        qs = super(ClienteListView, self).get_queryset()
        nome = self.request.GET.get('nome')
        cpf = self.request.GET.get('cpf')
        telefone = self.request.GET.get('telefone')
        categoria = self.request.GET.get('categoria')

        if nome:
            qs = qs.filter(nome__icontains=nome)
        if cpf:
            qs = qs.filter(cpf__icontains=cpf)
        if telefone:
            qs = qs.filter(telefone__icontains=telefone)
        if categoria:
            qs = qs.filter(categoria=categoria)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhum cliente encontrado com estes filtros!')


class ClienteCreateView(PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'clientes.add_cliente'
    permission_denied_message = 'Cadastrar cliente'
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente cadastrado com sucesso!'


class ClienteUpdateView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'clientes.update_cliente'
    permission_denied_message = 'Atualizar cliente'
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente alterado com sucesso!'


class ClienteDeleteView(PermissionRequiredMixin,SuccessMessageMixin, DeleteView):
    permission_required = 'clientes.delete_cliente'
    permission_denied_message = 'Deletar cliente'
    model = Cliente
    template_name = 'cliente_apagar.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente apagado com sucesso!'