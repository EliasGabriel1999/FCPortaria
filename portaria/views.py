import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import connection
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from portaria.forms import LoginForm

# ----LOGIN PAGE---- #
from core.models import Visitante, Visita, Usuario, FornecedorVisitante, Loja, Fornecedor


class PortariaLoginView(LoginView):
    form_class = LoginForm
    redirect_authenticated_user = True
    template_name = 'portaria_login.html'
    login_url = reverse_lazy('portaria:portaria_login')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form.add_error('username', '')
        form.add_error('password', '')
        return response

    def get_success_url(self):
        return reverse_lazy('portaria:portaria_home')


# ----HOME PAGE---- #
@method_decorator(login_required(login_url=reverse_lazy('portaria:portaria_login')), name='dispatch')
class PortariaHomeView(TemplateView):
    template_name = 'portaria_home.html'

    # -- RETURN CONTEXT VIEW -- #
    def get_context_data(self, **kwargs):
        context = super(PortariaHomeView, self).get_context_data(**kwargs)
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id_loja FROM core_usuario WHERE 1 = 1 and login = '{self.request.user}'")
            row = cursor.fetchone()

        id_loja = row[0]
        context['usuario'] = self.request.user
        context['qtvisitantes'] = Visita.objects.filter(datalanc=datetime.datetime.today(), saida__isnull=True,
                                                        id_loja=id_loja).count()

        return context


# ----ENTRADA PAGE---- #
@method_decorator(login_required(login_url=reverse_lazy('portaria:portaria_login')), name='dispatch')
class PortariaEntradaView(ListView):
    model = Visitante
    context_object_name = 'visitantes'
    template_name = 'portaria_entrada.html'

    # -- RETURN QUERYSET CONTENT -- #
    def get_queryset(self):
        queryset = super().get_queryset()
        filtro = self.request.GET.get('filtro')
        if filtro:
            queryset = Visitante.objects.filter(Q(nome__icontains=filtro) | Q(cpf__exact=filtro))
        else:
            queryset = queryset.none()
        return queryset

    # -- RETURN CONTEXT VIEW -- #
    def get_context_data(self, **kwargs):
        context = super(PortariaEntradaView, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user

        return context


@method_decorator(login_required(login_url=reverse_lazy('portaria:portaria_login')), name='dispatch')
class PortariaLancaEntradaView(CreateView):
    model = Visita
    template_name = 'portaria_lancentrada.html'
    fields = ['id_loja', 'id_visitante', 'id_fornecedor']
    success_url = reverse_lazy('portaria:portaria_home')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id_loja FROM core_usuario WHERE 1 = 1 and login = '{self.request.user}'")
            row = cursor.fetchone()

        id_loja = row[0]
        id_visitante = self.kwargs.get('id_visitante')
        form.fields['id_loja'].queryset = Loja.objects.filter(id=id_loja)
        form.fields['id_visitante'].queryset = Visitante.objects.filter(id=id_visitante)
        form.fields['id_fornecedor'].queryset = Fornecedor.objects.filter(
            id__in=FornecedorVisitante.objects.filter(id_visitante=id_visitante).values_list('id_fornecedor',
                                                                                             flat=True))
        form.fields['id_loja'].disabled = True
        form.fields['id_visitante'].disabled = True
        return form

    def get_initial(self):
        initial = super().get_initial()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id_loja FROM core_usuario WHERE 1 = 1 and login = '{self.request.user}'")
            row = cursor.fetchone()

        id_loja = row[0]
        id_visitante = self.kwargs.get('id_visitante')
        initial['id_loja'] = id_loja
        initial['id_visitante'] = id_visitante
        return initial

    def form_valid(self, form):
        messages.success(self.request, 'Entrada realizada com sucesso!')
        id_visitante = self.kwargs.get('id_visitante')
        id_fornecedor = self.request.POST.get('id_fornecedor')
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id_loja FROM core_usuario WHERE 1 = 1 and login = '{self.request.user}'")
            row = cursor.fetchone()
        id_loja = row[0]
        data = datetime.datetime.today()
        visita = Visita.objects.filter(id_loja=id_loja, id_visitante=id_visitante, id_fornecedor=id_fornecedor,
                                       datalanc=data).count()
        if visita > 0:
            form.add_error(None, 'Visitante já deu entrada para esse fornecedor.')
            form.add_error('id_fornecedor', '')
            return self.form_invalid(form)
        form.instance.datalanc = datetime.datetime.today().date()
        form.instance.entrada = datetime.datetime.today().strftime('%H:%M:%S')
        return super().form_valid(form)


# ----SAIDA PAGE---- #
@method_decorator(login_required(login_url=reverse_lazy('portaria:portaria_login')), name='dispatch')
class PortariaSaidaView(ListView):
    model = Visita
    context_object_name = 'visitantes'
    template_name = 'portaria_saida.html'

    # -- RETURN QUERYSET CONTENT -- #
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('id_visitante')
        filtro = self.request.GET.get('filtro')
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id_loja FROM core_usuario WHERE 1 = 1 and login = '{self.request.user}'")
            row = cursor.fetchone()
        id_loja = row[0]

        if filtro:
            visitante = Visitante.objects.filter(Q(nome__icontains=filtro) | Q(cpf__exact=filtro))
            queryset = Visita.objects.filter(
                id_loja=id_loja, datalanc=datetime.datetime.today(),
                id_visitante__in=visitante, saida__isnull=True).select_related('id_visitante', 'id_fornecedor').values('id', 'id_visitante__nome', 'id_fornecedor__razaosocial', 'id_visitante__id', 'id_visitante__cpf', 'id_fornecedor__cnpj', 'id_fornecedor__id')
        else:
            queryset = queryset.none()
        return queryset

    # -- RETURN CONTEXT VIEW -- #
    def get_context_data(self, **kwargs):
        context = super(PortariaSaidaView, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user

        return context


@method_decorator(login_required(login_url=reverse_lazy('portaria:portaria_login')), name='dispatch')
class PortariaLancaSaidaView(UpdateView):
    model = Visita
    template_name = 'portaria_lancsaida.html'
    fields = ['id_loja', 'id_visitante', 'id_fornecedor']
    success_url = reverse_lazy('portaria:portaria_home')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['id_loja'].disabled = True
        form.fields['id_visitante'].disabled = True
        form.fields['id_fornecedor'].disabled = True
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Saída realizada com sucesso!')
        form.instance.saida = datetime.datetime.today().strftime('%H:%M:%S')
        return super().form_valid(form)
