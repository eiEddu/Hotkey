
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Emprestimo


scheduler = BackgroundScheduler()
scheduler.start()

def job_alerta_atraso_especifico(emprestimo_id):
    try:
        emp = Emprestimo.objects.get(pk=emprestimo_id)

        if emp.status == 'ATIVO':
            emp.status = 'NOTIFICADO'
            emp.save()

            # Prepara os dados para mandar para os arquivos HTML e TXT
            dados = {
                'codigo_emprestimo': emp.codigo,
                'reserva_codigo': emp.reserva.codigo,
                'chave_codigo': emp.chave.codigo,
                'chave_bloco_codigo': emp.chave_bloco.codigo if emp.chave_bloco else None,
            }

            texto_email = render_to_string('emails/alerta_atraso.txt', dados)
            html_email = render_to_string('emails/alerta_atraso.html', dados)

            assunto = f"ALERTA CRÍTICO: Chaves retidas - Empréstimo {emp.codigo}"

            send_mail(
                subject=assunto,
                message=texto_email,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['corporativo.amaral@gmail.com'],
                html_message=html_email,
                fail_silently=True
            )
            print(f"Job executado: Status do empréstimo {emp.codigo} alterado para NOTIFICADO e e-mail enviado.")
    except Exception as e:
        print(f"Erro ao executar job de atraso: {e}")