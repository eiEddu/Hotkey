from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView
from .forms import EmprestimoQuartoForm, EmprestimoSalaComercialForm
from .models import Emprestimo
from chaves.models import Chave


class EmprestimoListView(ListView):
    model = Emprestimo
    template_name = 'emprestimos.html'

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super(EmprestimoListView, self).get_queryset()
        if buscar:
            qs = qs.filter(codigo__icontains=buscar)
        return qs


class EmprestimoQuartoCreateView(CreateView):
    model = Emprestimo
    form_class = EmprestimoQuartoForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')

    def form_valid(self, form):
        reserva = form.cleaned_data['reserva']
        chave = Chave.objects.filter(sala=reserva.sala, status='DISPONÍVEL').first()

        if not chave:
            messages.error(self.request, f"ERRO: Não há chaves disponíveis para a sala {reserva.sala.codigo}")
            return self.form_invalid(form)

        form.instance.cliente = form.cleaned_data['cliente']
        form.instance.chave = chave
        form.instance.data_inicio = timezone.now()
        form.instance.data_devolucao = reserva.data_fim

        chave.status = 'EMPRESTADA'
        chave.save()

        messages.success(self.request, f"Empréstimo realizado! ENTREGUE A CHAVE: {chave.codigo}")
        return super().form_valid(form)


class EmprestimoSalaComercialCreateView(CreateView):
    model = Emprestimo
    form_class = EmprestimoSalaComercialForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')

    def form_valid(self, form):
        reserva = form.cleaned_data['reserva']
        chave_s = Chave.objects.filter(sala=reserva.sala, status='DISPONÍVEL').first()
        chave_b = Chave.objects.filter(bloco=reserva.sala.bloco, status='DISPONÍVEL').first()

        if not chave_s or not chave_b:
            messages.error(self.request, "ERRO: Chave da sala ou do bloco indisponível!")
            return self.form_invalid(form)

        form.instance.cliente = form.cleaned_data['cliente']
        form.instance.chave = chave_s
        form.instance.chave_bloco = chave_b
        form.instance.data_inicio = timezone.now()
        form.instance.data_devolucao = reserva.data_fim

        chave_s.status = 'EMPRESTADA'
        chave_s.save()
        chave_b.status = 'EMPRESTADA'
        chave_b.save()

        messages.success(self.request, f"Empréstimo realizado! ENTREGAR CHAVES: {chave_s.codigo} e {chave_b.codigo}")
        return super().form_valid(form)


class EmprestimoDeleteView(DeleteView):
    model = Emprestimo
    template_name = 'emprestimo_apagar.html'
    success_url = reverse_lazy('emprestimos')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Registro de empréstimo removido com sucesso.")
        return super().delete(request, *args, **kwargs)


class EmprestimoDevolucaoView(View):
    def get(self, request, pk):
        emprestimo = Emprestimo.objects.get(pk=pk)
        emprestimo.status = 'FINALIZADO/DEVOLVIDO'

        emprestimo.chave.status = 'DISPONÍVEL'
        emprestimo.chave.save()

        if emprestimo.chave_bloco:
            emprestimo.chave_bloco.status = 'DISPONÍVEL'
            emprestimo.chave_bloco.save()

        emprestimo.save()
        messages.success(request, f"Empréstimo {emprestimo.codigo} finalizado e chaves liberadas com sucesso!")
        return redirect('emprestimos')