from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView
from .jobs import scheduler, job_alerta_atraso_especifico
from pi_hotkey import settings
from .forms import EmprestimoQuartoForm, EmprestimoSalaComercialForm
from .models import Emprestimo
from chaves.models import Chave
from datetime import timedelta

class EmprestimoListView(PermissionRequiredMixin,ListView):
    permission_required = 'emprestimos.view_emprestimo'
    permission_denied_message = 'Visualizar empréstimo'
    model = Emprestimo
    template_name = 'emprestimos.html'

    def get_queryset(self):

        ##################### FILTROS DE BUSCA #####################
        qs = super(EmprestimoListView, self).get_queryset()
        codigo = self.request.GET.get('codigo')
        data = self.request.GET.get('data')
        cliente = self.request.GET.get('cliente')
        funcionario = self.request.GET.get('funcionario')
        chave_sala = self.request.GET.get('chave_sala')
        chave_bloco = self.request.GET.get('chave_bloco')
        status = self.request.GET.get('status')

        if codigo:
            qs = qs.filter(codigo__icontains=codigo)
        if cliente:
            qs = qs.filter(cliente__nome__icontains=cliente)
        if funcionario:
            qs = qs.filter(funcionario__nome__icontains=funcionario)
        if chave_sala:
            qs = qs.filter(chave__codigo__icontains=chave_sala)
        if chave_bloco:
            qs = qs.filter(chave_bloco__codigo__icontains=chave_bloco)
        if status:
            qs = qs.filter(status=status)
        if data:
            qs = qs.filter(data_inicio__date__lte=data, data_devolucao__date__gte=data)

        if qs.count() > 0:
            paginator = Paginator(qs, 10)
            listagem = paginator.get_page(self.request.GET.get('page'))
            return listagem
        else:
            return messages.info(self.request, 'Nenhum empréstimo encontrado com estes filtros!')


class EmprestimoQuartoCreateView(PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    permission_required = 'emprestimos.add_emprestimo'
    permission_denied_message = 'Cadastrar empréstimo'
    model = Emprestimo
    form_class = EmprestimoQuartoForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')

    def form_valid(self, form):
        reserva = form.cleaned_data['reserva']
        cliente = form.cleaned_data['cliente']

        ############################################
        ###### VERIFICAÇÃO DE CHAVES EM ATRASO #####
        ############################################
        tem_atraso = Emprestimo.objects.filter(
            cliente=cliente, status='ATIVO', data_devolucao__lt=timezone.now()
        ).exists()
        if tem_atraso:
            messages.error(self.request, "BLOQUEIO: O cliente possui chaves com entrega em atraso!")
            return self.form_invalid(form)

        ####################################################
        ######## VERIFICAÇÃO DE 1a CHAVE DISPONÍVEL ########
        ####################################################
        chave = Chave.objects.filter(sala=reserva.sala, status='DISPONÍVEL').first()

        if not chave:
            messages.error(self.request, f"ERRO: Não há chaves disponíveis para a sala {reserva.sala.codigo}")
            return self.form_invalid(form)

        ##########################################################
        ######## BUSCA AUTOMÁTICA PARA OS CHOICES NO FORM ########
        ##########################################################
        form.instance.cliente = form.cleaned_data['cliente']
        form.instance.chave = chave
        form.instance.data_inicio = timezone.now()
        form.instance.data_devolucao = reserva.data_fim

        chave.status = 'EMPRESTADA'
        chave.save()
        messages.success(self.request, f"Empréstimo realizado! ENTREGUE A CHAVE: {chave.codigo}")
        enviar_email_emprestimo(form.instance)

        ###############################################################
        ######## JOB PARA AVISO DE CHAVES NÃO DEVOLVIDAS (24H) ########
        ###############################################################
        resultado = super().form_valid(form)
        data_alerta = self.object.data_devolucao + timedelta(minutes=1)
        scheduler.add_job(
            job_alerta_atraso_especifico,
            trigger='date',
            run_date=data_alerta,
            args=[self.object.id],
            id=f"alerta_emprestimo_{self.object.id}",
            replace_existing=True
        )
        print(f"Alerta de atraso configurado para: {data_alerta.strftime('%d/%m/%Y %H:%M:%S')}") #Debug no Terminal
        return resultado


class EmprestimoSalaComercialCreateView(PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    permission_required = 'emprestimos.add_emprestimo'
    permission_denied_message = 'Cadastrar empréstimo'
    model = Emprestimo
    form_class = EmprestimoSalaComercialForm
    template_name = 'emprestimo_form.html'
    success_url = reverse_lazy('emprestimos')

    def form_valid(self, form):
        reserva = form.cleaned_data['reserva']
        cliente = form.cleaned_data['cliente']

        ############################################
        ###### VERIFICAÇÃO DE CHAVES EM ATRASO #####
        ############################################
        tem_atraso = Emprestimo.objects.filter(
            cliente=cliente, status='ATIVO', data_devolucao__lt=timezone.now()
        ).exists()
        if tem_atraso:
            messages.error(self.request, "BLOQUEIO: O cliente possui chaves com entrega em atraso!")
            return self.form_invalid(form)

        #############################################
        ####### CONTADOR PARA CHAVES DE BLOCO #######
        #############################################
        chaves_bloco_disponiveis = Chave.objects.filter(bloco=reserva.sala.bloco, status='DISPONÍVEL').count()
        if chaves_bloco_disponiveis <= 1:
            messages.error(self.request, "BLOQUEIO: Apenas a cópia de emergência do bloco está disponível no estoque!")
            return self.form_invalid(form)

        ####################################################
        ######## VERIFICAÇÃO DE 1a CHAVE DISPONÍVEL ########
        ####################################################
        chave_s = Chave.objects.filter(sala=reserva.sala, status='DISPONÍVEL').first()
        chave_b = Chave.objects.filter(bloco=reserva.sala.bloco, status='DISPONÍVEL').first()
        if not chave_s or not chave_b:
            messages.error(self.request, "ERRO: Chave da sala ou do bloco indisponível!")
            return self.form_invalid(form)

        ##########################################################
        ######## BUSCA AUTOMÁTICA PARA OS CHOICES NO FORM ########
        ##########################################################
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
        enviar_email_emprestimo(form.instance)

        ###############################################################
        ######## JOB PARA AVISO DE CHAVES NÃO DEVOLVIDAS (24H) ########
        ###############################################################
        resultado = super().form_valid(form)
        data_alerta = self.object.data_devolucao + timedelta(minutes=1)
        scheduler.add_job(
            job_alerta_atraso_especifico,
            trigger='date',
            run_date=data_alerta,
            args=[self.object.id],
            id=f"alerta_emprestimo_{self.object.id}",
            replace_existing=True
        )
        print(f"Alerta de atraso configurado para: {data_alerta.strftime('%d/%m/%Y %H:%M:%S')}")
        return resultado


class EmprestimoDeleteView(PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    model = Emprestimo
    template_name = 'emprestimo_apagar.html'
    success_url = reverse_lazy('emprestimos')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Registro de empréstimo removido com sucesso.")
        return super().delete(request, *args, **kwargs)


############################################################
########## ALTERAR STATUS DAS CHAVES NA DEVOLUÇÃO ##########
############################################################
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


#############################################################
########## CONFIGS DO ENVIO DE EMAIL NO EMPRESTIMO ##########
#############################################################
def enviar_email_emprestimo(emprestimo):
    dados = {
        'cliente': emprestimo.cliente.nome,
        'codigo_emprestimo': emprestimo.codigo,
        'reserva_codigo': emprestimo.reserva.codigo,
        'chave_codigo': emprestimo.chave.codigo,
        'chave_bloco_codigo': emprestimo.chave_bloco.codigo if emprestimo.chave_bloco else None,
        'data_devolucao': emprestimo.data_devolucao.strftime("%d/%m/%Y às %H:%M")
    }
    texto_email = render_to_string('emails/texto_email.txt', dados)
    html_email = render_to_string('emails/texto_email.html', dados)
    send_mail(
        subject=f"HOTKEY - Confirmação de Retirada de Chave ({dados['chave_codigo']})",
        message=texto_email,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[emprestimo.cliente.email],
        html_message=html_email,
        fail_silently=False
    )
    return redirect('emprestimos')