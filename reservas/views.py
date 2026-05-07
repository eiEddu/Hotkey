from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import ReservaQuartoForm, ReservaSalaComercialForm
from .models import Reserva

class ReservaListView(ListView):
    model = Reserva
    template_name = 'reservas.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(ReservaListView, self).get_queryset()

        if buscar:
            qs = qs.filter(codigo__icontains=buscar)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Não existem reservas!')

class ReservaQuartoCreateView(SuccessMessageMixin, CreateView):
    model = Reserva
    form_class = ReservaQuartoForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva de Quarto criada com sucesso!'

class ReservaSalaComercialCreateView(SuccessMessageMixin, CreateView):
    model = Reserva
    form_class = ReservaSalaComercialForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva de Sala Comercial criada com sucesso!'

class ReservaQuartoUpdateView(SuccessMessageMixin, UpdateView):
    model = Reserva
    form_class = ReservaQuartoForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva atualizada com sucesso!'

class ReservaSalaComercialUpdateView(SuccessMessageMixin, UpdateView):
    model = Reserva
    form_class = ReservaSalaComercialForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva atualizada com sucesso!'

class ReservaDeleteView(SuccessMessageMixin, DeleteView):
    model = Reserva
    template_name = 'reserva_apagar.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva apagada com sucesso!'