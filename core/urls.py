from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import HomeView, CustomLoginView, VisitantesView, VisitanteDeleteView, VisitanteUpdateView, \
    VisitanteCreateView, RedeView, RedeVinculoView, RedeDesvinculaView, RedeInsereVinculo, RelatorioVisitaView, PdfView

app_name = 'core'

urlpatterns = [
    path("futurecode/login", CustomLoginView.as_view(), name='login'),
    path("futurecode/home", HomeView.as_view(), name='home'),
    path("futurecode/visitantes", VisitantesView.as_view(), name='visitantes'),
    path("futurecode/criar_visitante", VisitanteCreateView.as_view(), name='criar_visitantes'),
    path("futurecode/editar_visitante/<int:pk>", VisitanteUpdateView.as_view(), name='editar_visitante'),
    path("futurecode/delete_visitante/<int:pk>", VisitanteDeleteView.as_view(), name='delete_visitante'),
    path("futurecode/rede", RedeView.as_view(), name='rede'),
    path("futurecode/rede/insere_visitante", RedeInsereVinculo.as_view(), name='insere_visitante'),
    path("futurecode/rede/<int:pk>", RedeVinculoView.as_view(), name='rede_vinculo'),
    path('futurecode/rede/deletar/<int:id>', RedeDesvinculaView.as_view(), name='desvincula_rede'),
    path('futurecode/visitas', RelatorioVisitaView.as_view(), name='relatorio_visita'),
    path('futurecode/visitas/gerarrelatorio', PdfView.as_view(), name='relatorio_pdf'),
    path('logout/', LogoutView.as_view(next_page='/futurecode/login'), name='logout')
]
