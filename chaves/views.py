from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import ChaveBlocoModelForm, ChaveQuartoModelForm, ChaveSalaComercialModelForm
from .models import Chave

class ChaveListView(ListView):
    model = Chave
    template_name = 'chaves.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ChaveListView, self).get_queryset()

        if buscar:
            qs = qs.filter(codigo__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 5)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem chaves cadastradas!')

class ChaveBlocoCreateView(SuccessMessageMixin, CreateView):
    model = Chave
    form_class = ChaveBlocoModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave de Bloco cadastrada com sucesso!'

    def form_valid(self, form):
        form.instance.tipo = 'BLOCO'
        return super().form_valid(form)

class ChaveQuartoCreateView(SuccessMessageMixin, CreateView):
    model = Chave
    form_class = ChaveQuartoModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave de Quarto cadastrada com sucesso!'

    def form_valid(self, form):
        form.instance.tipo = 'SALA'
        return super().form_valid(form)

class ChaveSalaComercialCreateView(SuccessMessageMixin, CreateView):
    model = Chave
    form_class = ChaveSalaComercialModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave de Sala Comercial cadastrada com sucesso!'

    def form_valid(self, form):
        form.instance.tipo = 'SALA'
        return super().form_valid(form)

class ChaveUpdateView(SuccessMessageMixin, UpdateView):
    model = Chave
    form_class = ChaveSalaComercialModelForm
    template_name = 'chave_form.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave atualizada com sucesso!'


class ChaveDeleteView(SuccessMessageMixin, DeleteView):
    model = Chave
    template_name = 'chave_apagar.html'
    success_url = reverse_lazy('chaves')
    success_message = 'Chave apagada com sucesso!'