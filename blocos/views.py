from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from blocos.forms import BlocoModelForm
from blocos.models import Bloco


class BlocoListView(ListView):
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

class BlocoCreateView(CreateView):
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

class BlocoUpdateView(UpdateView):
    model = Bloco
    form_class = BlocoModelForm
    template_name = 'bloco_form.html'
    success_url = reverse_lazy('blocos')
    success_message = 'Bloco atualizado com sucesso!'

class BlocoDeleteView(DeleteView):
    model = Bloco
    template_name = 'bloco_apagar.html'
    success_url = reverse_lazy('blocos')
    success_message = 'Bloco apagado com sucesso!'