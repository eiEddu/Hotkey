from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from blocos.forms import BlocoModelForm
from blocos.models import Bloco


class BlocoListView(PermissionRequiredMixin,ListView):
    permission_required = 'blocos.view_bloco'
    permission_denied_message = 'Visualizar bloco'
    model = Bloco
    template_name = 'blocos.html'


    def get_queryset(self):

        #######################################
        ########## FILTROS DE BUSCA ###########
        #######################################
        qs = super(BlocoListView, self).get_queryset()
        codigo = self.request.GET.get('codigo')
        andar = self.request.GET.get('andar')
        nome = self.request.GET.get('nome')

        if codigo:
            qs = qs.filter(codigo__icontains=codigo)
        if andar:
            qs = qs.filter(andar=andar)
        if nome:
            qs = qs.filter(nome__icontains=nome)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhum bloco encontrado com estes filtros!')


class BlocoCreateView(PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    permission_required = 'blocos.add_bloco'
    permission_denied_message = 'Cadastrar bloco'
    model = Bloco
    form_class = BlocoModelForm
    template_name = 'bloco_form.html'
    success_url = reverse_lazy('blocos')
    success_message = 'Bloco cadastrado com sucesso!'

    ###################################################
    ########## CRIAÇÃO AUTOMÁTICA DE CÓDIGO ###########
    ###################################################
    def form_valid(self, form):
        response = super().form_valid(form)
        codigo = "AN"+form.cleaned_data['andar']+"BL"+str(self.object.pk)
        self.object.codigo = codigo
        self.object.save()
        return response

class BlocoUpdateView(PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    permission_required = 'blocos.update_bloco'
    permission_denied_message = 'Atualizar bloco'
    model = Bloco
    form_class = BlocoModelForm
    template_name = 'bloco_form.html'
    success_url = reverse_lazy('blocos')
    success_message = 'Bloco atualizado com sucesso!'

class BlocoDeleteView(PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    permission_required = 'blocos.delete_bloco'
    permission_denied_message = 'Deletar bloco'
    model = Bloco
    template_name = 'bloco_apagar.html'
    success_url = reverse_lazy('blocos')
    success_message = 'Bloco apagado com sucesso!'

    ##########################################################
    ########## ALTERAR MENSAGEM DE ERRO NA EXCLUSÃO ##########
    ##########################################################
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request,*args,**kwargs)
        except ProtectedError:
            messages.error(request,f'O bloco {self.object} não pode ser excluído. 'f'Este bloco possui salas e/ou chaves registradas!')
            return redirect('blocos')