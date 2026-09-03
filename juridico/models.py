from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models

class RegistroBase(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Advogado(RegistroBase):
    nome = models.CharField(max_length=160)
    oab = models.CharField("Matrícula da OAB", max_length=30, unique=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=25, blank=True)
    data_admissao = models.DateField()
    ativo = models.BooleanField(default=True)
    resumo_profissional = models.TextField("Contexto histórico")
    formacao = models.TextField(blank=True)
    especialidades = models.CharField(max_length=300, blank=True)
    def __str__(self): return f"{self.nome} — {self.oab}"
    class Meta: ordering = ["nome"]

class HistoricoAdvogado(RegistroBase):
    advogado = models.ForeignKey(Advogado, on_delete=models.CASCADE, related_name="historicos")
    data_evento = models.DateTimeField()
    titulo = models.CharField(max_length=150)
    descricao = models.TextField()
    def __str__(self): return f"{self.advogado.nome}: {self.titulo}"
    class Meta: ordering = ["-data_evento"]

class Processo(RegistroBase):
    AREAS = [
        ("PENAL", "Direito Penal"), ("TRIBUTARIO", "Direito Tributário"),
        ("TRABALHO", "Direito do Trabalho"), ("CIVIL", "Direito Civil"),
        ("FAMILIA", "Direito de Família"), ("CONSUMIDOR", "Direito do Consumidor"),
    ]
    STATUS = [
        ("NOVO", "Novo"), ("EM_ANDAMENTO", "Em andamento"), ("DEFERIDO", "Deferido"),
        ("INDEFERIDO", "Indeferido"), ("SUSPENSO", "Suspenso"), ("CONCLUIDO", "Concluído"),
    ]
    numero = models.CharField("Número do processo", max_length=40, unique=True)
    titulo = models.CharField(max_length=180)
    area = models.CharField(max_length=20, choices=AREAS)
    status = models.CharField(max_length=20, choices=STATUS, default="NOVO")
    advogado = models.ForeignKey(Advogado, on_delete=models.PROTECT, related_name="processos")
    parte_autora = models.CharField(max_length=180)
    parte_re = models.CharField("Parte ré", max_length=180)
    tribunal = models.CharField(max_length=150, blank=True)
    comarca = models.CharField(max_length=120, blank=True)
    data_distribuicao = models.DateField()
    prazo_atual = models.DateTimeField(null=True, blank=True)
    valor_causa = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    descricao = models.TextField(blank=True)
    def __str__(self): return f"{self.numero} — {self.titulo}"
    class Meta: ordering = ["-atualizado_em"]

class Andamento(RegistroBase):
    processo = models.ForeignKey(
        Processo,
        on_delete=models.CASCADE,
        related_name="andamentos"
    )

    data = models.DateTimeField()

    descricao = models.TextField()

    responsavel = models.CharField(
        max_length=150,
        blank=True
    )

    status_processo = models.CharField(
        "Novo status do processo",
        max_length=20,
        choices=Processo.STATUS,
        blank=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Se um novo status foi informado no andamento,
        # atualiza automaticamente o processo.
        if self.status_processo:
            Processo.objects.filter(
                pk=self.processo_id
            ).update(
                status=self.status_processo
            )

    def __str__(self):
        return (
            f"{self.processo.numero} — "
            f"{self.data:%d/%m/%Y}"
        )

    class Meta:
        ordering = ["-data"]

class DocumentoProcesso(RegistroBase):
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name="documentos")
    arquivo = models.FileField(upload_to="processos/%Y/%m/")
    nome_original = models.CharField(max_length=255)
    texto_extraido = models.TextField(blank=True)
    importado_automaticamente = models.BooleanField(default=True)
    def __str__(self): return self.nome_original
    class Meta: ordering = ["-criado_em"]

class Material(RegistroBase):
    UNIDADES = [("UN", "Unidade"), ("CX", "Caixa"), ("PCT", "Pacote"), ("RESMA", "Resma")]
    nome = models.CharField(max_length=140, unique=True)
    categoria = models.CharField(max_length=100)
    unidade = models.CharField(max_length=10, choices=UNIDADES, default="UN")
    quantidade = models.PositiveIntegerField(default=0)
    estoque_minimo = models.PositiveIntegerField(default=0)
    localizacao = models.CharField(max_length=100, blank=True)
    def __str__(self): return self.nome
    @property
    def estoque_baixo(self): return self.quantidade <= self.estoque_minimo
    class Meta: ordering = ["nome"]

class MovimentacaoEstoque(RegistroBase):
    TIPOS = [("ENTRADA", "Entrada"), ("SAIDA", "Saída")]
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name="movimentacoes")
    tipo = models.CharField(max_length=10, choices=TIPOS)
    quantidade = models.PositiveIntegerField()
    observacao = models.CharField(max_length=250, blank=True)
    def clean(self):
        if self.tipo == "SAIDA" and self.material_id and self.quantidade > self.material.quantidade:
            raise ValidationError("A saída não pode ser maior que o estoque disponível.")
    def save(self, *args, **kwargs):
        self.full_clean()
        novo = self._state.adding
        super().save(*args, **kwargs)
        if novo:
            sinal = 1 if self.tipo == "ENTRADA" else -1
            Material.objects.filter(pk=self.material_id).update(quantidade=models.F("quantidade") + sinal * self.quantidade)
    def __str__(self): return f"{self.get_tipo_display()} — {self.material.nome}"
    class Meta: ordering = ["-criado_em"]

class PeticaoIA(RegistroBase):
    TIPOS = [
        ("INICIAL", "Petição inicial"), ("CONTESTACAO", "Contestação"),
        ("REPLICA", "Réplica"), ("RECURSO", "Recurso"),
        ("AGRAVO", "Agravo"), ("MANIFESTACAO", "Manifestação"),
        ("CUMPRIMENTO", "Cumprimento de sentença"), ("EMBARGOS", "Embargos"),
        ("OUTROS", "Outros"),
    ]
    STATUS = [("RASCUNHO", "Rascunho gerado pela IA"), ("REVISAO", "Em revisão"), ("APROVADA", "Aprovada pelo advogado")]
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name="peticoes_ia")
    advogado = models.ForeignKey(Advogado, on_delete=models.PROTECT, related_name="peticoes_ia")
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name="peticoes_criadas")
    tipo = models.CharField(max_length=20, choices=TIPOS)
    objetivo = models.TextField()
    fatos_complementares = models.TextField(blank=True)
    fundamentos_sugeridos = models.TextField(blank=True)
    pedidos_especificos = models.TextField(blank=True)
    orientacoes = models.TextField(blank=True)
    texto_gerado = models.TextField(blank=True)
    modelo_utilizado = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=15, choices=STATUS, default="RASCUNHO")
    revisado_em = models.DateTimeField(null=True, blank=True)
    def __str__(self): return f"{self.get_tipo_display()} — {self.processo.numero}"
    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Petição elaborada com IA"
        verbose_name_plural = "Petições elaboradas com IA"
