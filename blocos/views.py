from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
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
        buscar = self.request.GET.get('buscar')
        qs = super(BlocoListView, self).get_queryset()

        if buscar:
            qs = qs.filter(codigo__icontains=buscar)

        if qs.count() >0:
            paginator = Paginator(qs, 5)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request,('Não existem blocos cadastrados!'))

class BlocoCreateView(PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    permission_required = 'blocos.add_bloco'
    permission_denied_message = 'Cadastrar bloco'
    model = Bloco
    form_class = BlocoModelForm
    template_name = 'bloco_form.html'
    success_url = reverse_lazy('blocos')
    success_message = 'Bloco cadastrado com sucesso!'

    def form_valid(self, form):
        self.object = form.save()
        codigo = "AN" + form.cleaned_data['andar'] + "BL" + str(self.object.pk)
        self.object.codigo = codigo
        self.object.save()

        return super().form_valid(form)

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