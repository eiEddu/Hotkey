from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import SalaModelForm
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
            return messages.info(self.request,'Não existem salas cadastradas!')

class SalaCreateView(CreateView):
    model = Sala
    form_class = SalaModelForm
    template_name = 'sala_form.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala criada com sucesso!'

class SalaUpdateView(SuccessMessageMixin, UpdateView):
    model = Sala
    form_class = SalaModelForm
    template_name = 'sala_form.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala alterada com sucesso!'


class SalaDeleteView(SuccessMessageMixin, DeleteView):
    model = Sala
    template_name = 'sala_apagar.html'
    success_url = reverse_lazy('salas')
    success_message = 'Sala apagada com sucesso!'