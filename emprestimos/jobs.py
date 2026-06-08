# emprestimos/jobs.py
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.conf import settings
from .models import Emprestimo

# 1. Inicializa o agendador e exporta a variável para ser usada nas views
scheduler = BackgroundScheduler()
scheduler.start()


# 2. A função do Job
def job_alerta_atraso_especifico(emprestimo_id):


    try:
        emp = Emprestimo.objects.get(pk=emprestimo_id)

        if emp.status == 'ATIVO':
            emp.status = 'NOTIFICADO'
            emp.save()

            chaves_texto = f"{emp.chave.codigo}"
            if emp.chave_bloco:
                chaves_texto += f" e {emp.chave_bloco.codigo}"

            assunto = f"ALERTA CRÍTICO: Chaves retidas - Empréstimo {emp.codigo}"
            mensagem = (
                f"Administrador,\n\n"
                f"O empréstimo {emp.codigo} vinculado à reserva {emp.reserva.codigo} "
                f"ultrapassou o limite de 24h após o encerramento.\n\n"
                f"As chaves {chaves_texto} constam como NÃO DEVOLVIDAS.\n"
                f"O status no sistema foi alterado para 'Ativo/Notificado'."
            )

            send_mail(
                subject=assunto,
                message=mensagem,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['corporativo.amaral@gmail.com'],
                fail_silently=True
            )
            print(f"Job executado: Status do empréstimo {emp.codigo} alterado para NOTIFICADO e e-mail enviado.")
    except Exception as e:
        print(f"Erro ao executar job de atraso: {e}")