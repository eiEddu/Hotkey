from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from .forms import ReservaQuartoForm, ReservaSalaComercialForm
from .models import Reserva
from django.shortcuts import redirect
from django.utils import timezone

class ReservaListView(PermissionRequiredMixin,ListView):
    permission_required = 'reservas.view_reserva'
    permission_denied = 'Visualizar reserva'
    model = Reserva
    template_name = 'reservas.html'

    def get_queryset(self):
        Reserva.objects.filter(status='ATIVA', data_fim__lt=timezone.now()).update(status='ENCERRADA')
        qs = super(ReservaListView, self).get_queryset()
        codigo = self.request.GET.get('codigo')
        data = self.request.GET.get('data')
        cliente = self.request.GET.get('cliente')
        sala = self.request.GET.get('sala')
        funcionario = self.request.GET.get('funcionario')
        status = self.request.GET.get('status')

        if codigo:
            qs = qs.filter(codigo__icontains=codigo)
        if cliente:
            qs = qs.filter(cliente__nome__icontains=cliente)
        if sala:
            qs = qs.filter(sala__codigo__icontains=sala)
        if funcionario:
            qs = qs.filter(funcionario__nome__icontains=funcionario)
        if status:
            qs = qs.filter(status=status)

        if data:
            qs = qs.filter(data_inicio__date__lte=data, data_fim__date__gte=data)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhuma reserva encontrada com estes filtros!')

class ReservaQuartoCreateView(PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'reservas.create_reserva'
    permission_denied = 'Cadastrar reserva de Quarto'
    model = Reserva
    form_class = ReservaQuartoForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva de Quarto criada com sucesso!'

class ReservaSalaComercialCreateView(PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'reservas.create_reserva'
    permission_denied = 'Cadastrar reserva de Sala Comercial'
    model = Reserva
    form_class = ReservaSalaComercialForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva de Sala Comercial criada com sucesso!'

class ReservaQuartoUpdateView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'reservas.update_reserva'
    permission_denied = 'Atualizar reserva de Quarto'
    model = Reserva
    form_class = ReservaQuartoForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva atualizada com sucesso!'

class ReservaSalaComercialUpdateView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'reservas.update_reserva'
    permission_denied = 'Atualizar reserva de Sala Comercial'
    model = Reserva
    form_class = ReservaSalaComercialForm
    template_name = 'reserva_form.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva atualizada com sucesso!'

class ReservaDeleteView(PermissionRequiredMixin,SuccessMessageMixin, DeleteView):
    permission_required = 'reservas.delete_reserva'
    permission_denied = 'Deletar reserva'
    model = Reserva
    template_name = 'reserva_apagar.html'
    success_url = reverse_lazy('reservas')
    success_message = 'Reserva apagada com sucesso!'

class ReservaEncerrarView(PermissionRequiredMixin, View):
    permission_required = 'reservas.update_reserva'

    def get(self, request, pk):
        reserva = Reserva.objects.get(pk=pk)
        reserva.status = 'ENCERRADA'
        reserva.save()
        messages.success(request, f"Reserva {reserva.codigo} encerrada com sucesso!")
        return redirect('reservas')