from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from blocos.models import Bloco
from .forms import QuartoModelForm, SalaComercialModelForm
from .models import Sala

class SalaListView(PermissionRequiredMixin,ListView):
    permission_required = 'salas.view_sala'
    permission_denied = 'Visualizar sala'
    model = Sala
    template_name = 'salas.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(SalaListView, self).get_queryset()
        if buscar:
            qs = qs.filter(codigo__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 5)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem salas cadastradas!')

class QuartoCreateView(PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'salas.create_sala'
    permission_denied = 'Criar Quarto'
    model = Sala
    form_class = QuartoModelForm
    template_name = 'sala_form.html'
    success_url = reverse_lazy('salas')
    success_message = 'Quarto criado com sucesso!'

    def form_valid(self, form):
        form.instance.tipo = 'QUARTO' # Define o tipo
        self.object = form.save()
        if self.object.pk < 10:
            codigo = "QU" + form.cleaned_data['andar'] + "0" + str(self.object.pk)
        else:
            codigo = "QU" + form.cleaned_data['andar'] + str(self.object.pk)
        self.object.codigo = codigo
        return super().form_valid(form)

class SalaComercialCreateView(PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'salas.create_sala'
    permission_denied = 'Criar Sala Comercial'
    model = Sala
    form_class = SalaComercialModelForm
    template_name = 'sala_form.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala Comercial criada com sucesso!'

    def form_valid(self, form):
        form.instance.tipo = 'SALA COMERCIAL' # Define o tipo
        self.object = form.save()
        codigo = form.cleaned_data['bloco'].codigo + "SA" + str(self.object.pk)
        self.object.codigo = codigo
        return super().form_valid(form)

class QuartoUpdateView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'salas.update_sala'
    permission_denied = 'Atualizar Quarto'
    model = Sala
    form_class = QuartoModelForm
    template_name = 'sala_form.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala alterada com sucesso!'

class SalaComercialUpdateView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'salas.update_sala'
    permission_denied = 'Atualizar Sala Comercial'
    model = Sala
    form_class = SalaComercialModelForm
    template_name = 'sala_form.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala alterada com sucesso!'

class SalaDeleteView(PermissionRequiredMixin,SuccessMessageMixin, DeleteView):
    permission_required = 'salas.delete_sala'
    permission_denied = 'Deletar Sala/Quarto'
    model = Sala
    template_name = 'sala_apagar.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala apagada com sucesso!'