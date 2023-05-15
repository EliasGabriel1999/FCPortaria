import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView


from core.forms import VisitanteForm, VisitanteUpdateForm, FornecedorVisitanteForm, LoginForm
from core.models import Visitante, SituacaoCadastro, FornecedorVisitante, Fornecedor, Visita, Loja


# ----LOGIN PAGE---- #
class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'
    form_class = LoginForm
    login_url = reverse_lazy('core:login')

    def form_invalid(self, form):
            response = super().form_invalid(form)
            form.add_error('username', '')
            form.add_error('password', '')
            return response

    def get_success_url(self):
        return reverse_lazy('core:home')


# ----HOME PAGE---- #
@method_decorator(login_required(login_url=reverse_lazy('core:login')), name='dispatch')
class HomeView(TemplateView):
    template_name = 'home.html'

    # -- RETURN CONTEXT VIEW -- #
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user

        return context


# ----VISITANTES PAGE---- #
@method_decorator(login_required(login_url=reverse_lazy('core:login')), name='dispatch')
class VisitantesView(ListView):
    model = Visitante
    context_object_name = 'visitantes'
    template_name = 'visitantes.html'

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
        context = super(VisitantesView, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user

        return context


@method_decorator(login_required(login_url=reverse_lazy('core:login')), name='dispatch')
class VisitanteCreateView(CreateView):
    model = Visitante
    form_class = VisitanteForm
    template_name = 'createvisitante.html'
    success_url = reverse_lazy('core:visitantes')

    def form_valid(self, form):
        messages.success(self.request, 'Visitante criado com sucesso!')
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('core:login')), name='dispatch')
class VisitanteUpdateView(UpdateView):
    model = Visitante
    form_class = VisitanteUpdateForm
    template_name = 'editvisitante.html'
    success_url = reverse_lazy('core:visitantes')

    def form_valid(self, form):
        cpf = form.cleaned_data.get('cpf')
        idVisitante = self.object.id
        visitante = Visitante.objects.filter(cpf=cpf).exclude(id=idVisitante).first()
        if visitante:
            form.add_error('cpf', 'CPF já cadastrado para outro usuário.')
            return self.form_invalid(form)
        messages.success(self.request, 'Visitante alterado com sucesso!')
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('core:login')), name='dispatch')
class VisitanteDeleteView(UpdateView):
    model = Visitante
    fields = ['id']
    template_name = 'deletevisitante.html'
    success_url = reverse_lazy('core:visitantes')

    def form_valid(self, form):
        messages.success(self.request, 'Visitante excluído com sucesso!')
        situacao_cadastro_id = 2
        situacao_cadastro = SituacaoCadastro.objects.get(pk=situacao_cadastro_id)
        form.instance.id_situacaocadastro = situacao_cadastro
        return super().form_valid(form)


# -- REDE VIEW -- #
@method_decorator(login_required(login_url=reverse_lazy('core:login')), name='dispatch')
class RedeView(ListView):
    model = Fornecedor
    context_object_name = 'fornecedor'
    template_name = 'rede.html'

    # -- RETURN QUERYSET CONTENT -- #
    def get_queryset(self):
        queryset = super().get_queryset()
        filtro = self.request.GET.get('filtro')
        idFiltro = self.request.GET.get('filroID')
        if filtro:
            queryset = Fornecedor.objects.filter(Q(razaosocial__icontains=filtro) | Q(cnpj__exact=filtro))
        elif idFiltro:
            queryset = Fornecedor.objects.filter(Q(id__exact=idFiltro))
        elif filtro and idFiltro:
            queryset = Fornecedor.objects.filter(
                Q(razaosocial__icontains=filtro) | Q(cnpj__exact=filtro) | Q(id__exact=idFiltro))
        else:
            queryset = queryset.none()
        return queryset

    # -- RETURN CONTEXT VIEW -- #
    def get_context_data(self, **kwargs):
        context = super(RedeView, self).get_context_data(**kwargs)
        context['usuario'] = self.request.user

        return context


# -- REDE VIEW -- #
@method_decorator(login_required(login_url=reverse_lazy('core:login')), name='dispatch')
class RedeVinculoView(TemplateView):
    template_name = 'vincularede.html'
    success_url = reverse_lazy('core:rede')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fornecedor'] = Fornecedor.objects.filter(id=self.kwargs['pk'])
        context['visitantes'] = FornecedorVisitante.objects.filter(id_fornecedor=self.kwargs['pk'])
        return context


@method_decorator(login_required(login_url=reverse_lazy('core:login')), name='dispatch')
class RedeDesvinculaView(DeleteView):
    model = FornecedorVisitante
    pk_url_kwarg = 'id'
    context_object_name = 'visitante'
    template_name = 'desvincularede.html'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f"Visitante foi desvinculado com sucesso.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        id_fornecedor = self.object.id_fornecedor_id
        return reverse_lazy('core:rede_vinculo', kwargs={'pk': id_fornecedor})


@method_decorator(login_required(login_url=reverse_lazy('core:login')), name='dispatch')
class RedeInsereVinculo(CreateView):
    model = FornecedorVisitante
    form_class = FornecedorVisitanteForm
    pk_url_kwarg = 'id'
    context_object_name = 'fornecedorvisitante'
    template_name = 'inserevisitante.html'

    def form_valid(self, form):
        id_fornecedor = form.cleaned_data.get('id_fornecedor')
        id_visitante = form.cleaned_data.get('id_visitante')
        retorno = FornecedorVisitante.objects.filter(id_fornecedor=id_fornecedor, id_visitante=id_visitante).first()
        if retorno:
            form.add_error('id_visitante', 'Visitante já vinculado para a rede informada.')
            return self.form_invalid(form)
        messages.success(self.request, 'Visitante vinculado com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        id_fornecedor = self.object.id_fornecedor_id
        return reverse_lazy('core:rede_vinculo', kwargs={'pk': id_fornecedor})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# ----RELATORIO VISITA PAGE---- #
@method_decorator(login_required(login_url=reverse_lazy('core:login')), name='dispatch')
class RelatorioVisitaView(ListView):
    model = Visita
    context_object_name = 'visitas'
    template_name = 'relatorio_visitas.html'

    # -- RETURN QUERYSET CONTENT -- #
    def get_queryset(self):
        queryset = super().get_queryset()
        id_loja = self.request.GET.get('loja')
        filtro = self.request.GET.get('filtro')
        fornecedor = self.request.GET.get('fornecedor')
        dtini = self.request.GET.get('dtini')
        dtfim = self.request.GET.get('dtfim')

        if filtro and id_loja and dtini and dtfim:
            queryset = Visita.objects.filter(
                id_loja=id_loja, datalanc__range=[dtini, dtfim],
                id_visitante=filtro, id_fornecedor=fornecedor).select_related('id_visitante', 'id_fornecedor').values('id', 'datalanc',
                'entrada', 'saida', 'id_visitante__nome', 'id_fornecedor__razaosocial', 'id_visitante__id',
                'id_visitante__cpf', 'id_fornecedor__cnpj', 'id_fornecedor__id').order_by('datalanc')
        else:
            queryset = queryset.none()
        return queryset

    # -- RETURN CONTEXT VIEW -- #
    def get_context_data(self, **kwargs):
        context = super(RelatorioVisitaView, self).get_context_data(**kwargs)
        context['lojas'] = Loja.objects.all().order_by('descricao')
        context['visitantes'] = Visitante.objects.all().order_by('id')
        context['fornecedores'] = Fornecedor.objects.all().order_by('id')
        context['usuario'] = self.request.user
        return context


@method_decorator(login_required(login_url=reverse_lazy('core:login')), name='dispatch')
class PdfView(TemplateView):
    template_name = "report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_loja = self.request.GET.get('id_loja')
        filtro = self.request.GET.get('filtro')
        fornecedor = self.request.GET.get('fornecedor')
        dtini = self.request.GET.get('dtini')
        dtfim = self.request.GET.get('dtfim')
        if id_loja and filtro and fornecedor and dtini and dtfim:
            context['visitas'] = Visita.objects.filter(id_visitante=filtro, id_loja=id_loja, id_fornecedor=fornecedor, datalanc__range=[dtini, dtfim])
            context['fornecedor'] = Fornecedor.objects.filter(id=fornecedor).first()
            context['visitante'] = Visitante.objects.filter(id=filtro).values('id', 'nome').first()
            context['dtemissao'] = datetime.datetime.today()
            context['loja'] = Loja.objects.filter(id=id_loja).first()
            context['dtini'] = dtini
            context['dtfim'] = dtfim
            return context
        else:
            messages.error(self.request, 'Informar os filtros para gerar o PDF.')
            return {}
