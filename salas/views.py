from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import QuartoModelForm, SalaComercialModelForm
from .models import Sala

class SalaListView(ListView):
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

class QuartoCreateView(SuccessMessageMixin, CreateView):
    model = Sala
    form_class = QuartoModelForm
    template_name = 'sala_form.html'
    success_url = reverse_lazy('salas')
    success_message = 'Quarto criado com sucesso!'

    def form_valid(self, form):
        form.instance.tipo = 'QUARTO' # Define o tipo
        return super().form_valid(form)

class SalaComercialCreateView(SuccessMessageMixin, CreateView):
    model = Sala
    form_class = SalaComercialModelForm
    template_name = 'sala_form.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala Comercial criada com sucesso!'

    def form_valid(self, form):
        form.instance.tipo = 'SALA COMERCIAL' # Define o tipo
        return super().form_valid(form)

class SalaUpdateView(SuccessMessageMixin, UpdateView):
    model = Sala
    form_class = SalaComercialModelForm
    template_name = 'sala_form.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala alterada com sucesso!'

class SalaDeleteView(SuccessMessageMixin, DeleteView):
    model = Sala
    template_name = 'sala_apagar.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala apagada com sucesso!'