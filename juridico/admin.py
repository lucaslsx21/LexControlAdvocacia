from django.contrib import admin
from .models import Advogado, Andamento, DocumentoProcesso, HistoricoAdvogado, Material, MovimentacaoEstoque, PeticaoIA, Processo

@admin.register(Advogado)
class AdvogadoAdmin(admin.ModelAdmin): list_display = ("nome", "oab", "email", "ativo"); search_fields = ("nome", "oab")
@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin): list_display = ("numero", "titulo", "area", "status", "advogado"); list_filter = ("area", "status"); search_fields = ("numero", "parte_autora", "parte_re")
admin.site.register([Andamento, DocumentoProcesso, HistoricoAdvogado, Material, MovimentacaoEstoque])

@admin.register(PeticaoIA)
class PeticaoIAAdmin(admin.ModelAdmin):
    list_display = ("processo", "tipo", "advogado", "status", "criado_em")
    list_filter = ("tipo", "status", "criado_em")
    search_fields = ("processo__numero", "advogado__nome", "texto_gerado")
    readonly_fields = ("modelo_utilizado", "criado_em", "atualizado_em")
