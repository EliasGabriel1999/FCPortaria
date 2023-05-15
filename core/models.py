import hashlib
from django.db import models


class TipoUsuario(models.Model):
    descricao = models.CharField(max_length=20, verbose_name='Descricao')

    def __str__(self):
        return self.descricao


class TipoVisitante(models.Model):
    descricao = models.CharField(max_length=20, verbose_name='Descricao')

    def __str__(self):
        return self.descricao


class SituacaoCadastro(models.Model):
    descricao = models.CharField(max_length=20, verbose_name='Descricao')

    def __str__(self):
        return self.descricao


class Loja(models.Model):
    descricao = models.CharField(max_length=25, verbose_name='Descricao')

    def __str__(self):
        return self.descricao


class Usuario(models.Model):
    login = models.CharField(max_length=12, verbose_name='Login')
    nome = models.CharField(max_length=30, verbose_name='Nome')
    senha = models.CharField(max_length=128, verbose_name='Senha')
    id_tipousuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE, db_column='id_tipousuario',
                                       verbose_name='Tipo Usuário', related_name='tipo_usuario')
    id_situacaocadastro = models.ForeignKey(SituacaoCadastro, on_delete=models.CASCADE, db_column='id_situacaocadastro',
                                            verbose_name='Situacao', related_name='situacao_usuario')
    id_loja = models.ForeignKey(Loja, on_delete=models.CASCADE, db_column='id_loja', verbose_name='Loja')
    datahoraultimoacesso = models.DateTimeField(null=False, verbose_name='Data/Hora Ult. Acesso')

    def __str__(self):
        return f"{self.id} - {self.login}"

    def save(self, *args, **kwargs):
        self.senha = hashlib.md5(str(self.senha).encode()).hexdigest()
        super().save(*args, **kwargs)


class Visitante(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    cpf = models.CharField(db_column='cpf', unique=True, max_length=11, verbose_name='CPF')
    id_tipovisitante = models.ForeignKey(TipoVisitante, on_delete=models.CASCADE, db_column='id_tipovisitante',
                                         verbose_name='Tipo Visitante', related_name='tipo_visitante')
    id_situacaocadastro = models.ForeignKey(SituacaoCadastro, default=1, on_delete=models.CASCADE,
                                            db_column='id_situacaocadastro',
                                            verbose_name='Situação')

    def __str__(self):
        return f"{self.id} - {self.nome} {self.cpf}"


class Fornecedor(models.Model):
    razaosocial = models.CharField(max_length=150, verbose_name='Razão Social')
    nomefantasia = models.CharField(max_length=150, verbose_name='Nome Fantasia')
    cnpj = models.CharField(max_length=14, verbose_name='CNPJ')
    inscricaoestadual = models.CharField(max_length=14, verbose_name='Inscrição Estadual')

    def __str__(self):
        return f"{self.id} - {self.razaosocial} {self.cnpj}"


class FornecedorVisitante(models.Model):
    id_visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE, db_column='id_visitante',
                                     verbose_name='ID Visitante', related_name='cod_visitante')
    id_fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, db_column='id_fornecedor',
                                      verbose_name='ID Fornecedor')

    def __str__(self):
        return str(self.id_fornecedor)


class Visita(models.Model):
    id_loja = models.ForeignKey(Loja, on_delete=models.CASCADE, db_column='id_loja',
                                verbose_name='ID Loja', related_name='cod_loja')
    id_visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE, db_column='id_visitante',
                                     verbose_name='ID Visitante')
    id_fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, db_column='id_fornecedor',
                                      verbose_name='ID Fornecedor')
    datalanc = models.DateField()
    entrada = models.TimeField()
    saida = models.TimeField()

    def __str__(self):
        return str(self.id_visitante)

