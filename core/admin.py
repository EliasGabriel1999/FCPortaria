from django.contrib import admin

from .models import Loja, Usuario, SituacaoCadastro, Visitante, TipoVisitante, TipoUsuario, Fornecedor, \
    FornecedorVisitante, Visita


@admin.register(TipoVisitante)
class TipoVisitanteAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao']


@admin.register(TipoUsuario)
class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao']


@admin.register(SituacaoCadastro)
class SituacaoCadastroAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao']


@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao']


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'login', 'id_tipousuario', 'id_situacaocadastro']


@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'id_tipovisitante', 'id_situacaocadastro']


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['id', 'razaosocial', 'nomefantasia', 'cnpj', 'inscricaoestadual']


@admin.register(FornecedorVisitante)
class FornecedorVisitanteAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_fornecedor', 'id_visitante']


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_visitante', 'datalanc', 'entrada', 'saida']
