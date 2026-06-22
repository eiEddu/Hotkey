from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import ChaveBlocoModelForm, ChaveQuartoModelForm, ChaveSalaComercialModelForm
from .models import Chave
from django.db.models import Q, ProtectedError


class ChaveListView(PermissionRequiredMixin,ListView):
    permission_required = 'chaves.view_chave'
    permission_denied_message = 'Visualizar chave'
    model = Chave
    template_name = 'chaves.html'

    def get_queryset(self):

        #######################################
        ########## FILTROS DE BUSCA ###########
        #######################################
        qs = super(ChaveListView, self).get_queryset()
        codigo = self.request.GET.get('codigo')
        tipo = self.request.GET.get('tipo')
        vinculo = self.request.GET.get('vinculo')
        status = self.request.GET.get('status')

        if codigo:
            qs = qs.filter(codigo__icontains=codigo)
        if tipo:
            qs = qs.filter(tipo=tipo)
        if status:
            qs = qs.filter(status=status)
        if vinculo:
            qs = qs.filter(
                Q(bloco__codigo__icontains=vinculo) |
                Q(sala__codigo__icontains=vinculo) |
                Q(bloco__nome__icontains=vinculo) |
                Q(sala__nome__icontains=vinculo)
            )

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhuma chave encontrada com estes filtros!')


class ChaveBlocoCreateView(PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'chaves.add_chave'
    permission_denied_message = 'Cadastrar chave de Bloco'
    model = Chave
    form_class = ChaveBlocoModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave de Bloco cadastrada com sucesso!'

    ###################################################
    ########## CRIAÇÃO AUTOMÁTICA DE CÓDIGO ###########
    ###################################################
    def form_valid(self, form):
        form.instance.tipo = 'BLOCO'
        self.object = form.save()
        codigo = form.cleaned_data['bloco'].codigo + "CH" + str(self.object.pk)
        self.object.codigo = codigo
        return super().form_valid(form)

class ChaveQuartoCreateView(PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'chaves.add_chave'
    permission_denied_message = 'Cadastrar chave de Quarto'
    model = Chave
    form_class = ChaveQuartoModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave de Quarto cadastrada com sucesso!'

    ###################################################
    ########## CRIAÇÃO AUTOMÁTICA DE CÓDIGO ###########
    ###################################################
    def form_valid(self, form):
        form.instance.tipo = 'SALA'
        self.object = form.save()
        codigo = form.cleaned_data['sala'].codigo + "CH" + str(self.object.pk)
        self.object.codigo = codigo
        return super().form_valid(form)

class ChaveSalaComercialCreateView(PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'chaves.add_chave'
    permission_denied_message = 'Cadastrar chave de Sala Comercial'
    model = Chave
    form_class = ChaveSalaComercialModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave de Sala Comercial cadastrada com sucesso!'

    ###################################################
    ########## CRIAÇÃO AUTOMÁTICA DE CÓDIGO ###########
    ###################################################
    def form_valid(self, form):
        form.instance.tipo = 'SALA'
        self.object = form.save()
        codigo = str(form.cleaned_data['sala'].pk) + "CH" + str(self.object.pk)
        self.object.codigo = codigo
        return super().form_valid(form)

class ChaveBlocoUpdateView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'chaves.update_chave'
    permission_denied_message = 'Atualizar chave de Bloco'
    model = Chave
    form_class = ChaveBlocoModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave atualizada com sucesso!'

class ChaveQuartoUpdateView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'chaves.update_chave'
    permission_denied_message = 'Atualizar chave de Quarto'
    model = Chave
    form_class = ChaveQuartoModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave atualizada com sucesso!'

class ChaveSalaComercialUpdateView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'chaves.update_chave'
    permission_denied_message = 'Atualizar chave de Sala Comercial'
    model = Chave
    form_class = ChaveSalaComercialModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave atualizada com sucesso!'


class ChaveDeleteView(PermissionRequiredMixin,SuccessMessageMixin, DeleteView):
    required_permission = 'chaves.delete_chave'
    permission_required = 'Deletar chave'
    model = Chave
    template_name = 'chave_apagar.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave apagada com sucesso!'

    ##########################################################
    ########## ALTERAR MENSAGEM DE ERRO NA EXCLUSÃO ##########
    ##########################################################
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request,*args,**kwargs)
        except ProtectedError:
            messages.error(request,f'A chave {self.object} não pode ser excluída. 'f'Esta chave está vinculada a um bloco/sala!')
