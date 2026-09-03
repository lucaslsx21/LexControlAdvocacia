from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path("advogados/", views.advogados, name="advogados"),

    path(
        "advogados/novo/",
        views.advogado_novo,
        name="advogado_novo"
    ),

    path(
        "advogados/<int:pk>/",
        views.advogado_detalhe,
        name="advogado_detalhe"
    ),

    path(
        "advogados/<int:pk>/editar/",
        views.advogado_editar,
        name="advogado_editar"
    ),

    path(
        "advogados/<int:pk>/excluir/",
        views.advogado_excluir,
        name="advogado_excluir"
    ),

    path(
    "exportar/<str:modulo>/<str:formato>/",
    views.exportar,
    name="exportar"
),


    path(
        "processos/",
        views.processos,
        name="processos"
    ),

    path(
        "processos/novo/",
        views.processo_novo,
        name="processo_novo"
    ),

    path(
        "processos/importar/",
        views.processo_importar,
        name="processo_importar"
    ),

    path(
        "processos/<int:pk>/",
        views.processo_detalhe,
        name="processo_detalhe"
    ),

    path(
        "processos/<int:pk>/editar/",
        views.processo_editar,
        name="processo_editar"
    ),

    path(
        "processos/<int:pk>/excluir/",
        views.processo_excluir,
        name="processo_excluir"
    ),


    path(
        "andamentos/novo/",
        views.andamento_novo,
        name="andamento_novo"
    ),


    # =====================================================
    # ASSISTENTE DE PETIÇÕES COM IA
    # =====================================================

    path(
        "peticoes/",
        views.peticoes_ia,
        name="peticoes_ia"
    ),

    path(
        "processos/<int:processo_id>/peticao/nova/",
        views.peticao_ia_nova,
        name="peticao_ia_nova"
    ),

    path(
        "peticoes/<int:pk>/",
        views.peticao_ia_detalhe,
        name="peticao_ia_detalhe"
    ),

    path(
        "peticoes/<int:pk>/revisar/",
        views.peticao_ia_revisar,
        name="peticao_ia_revisar"
    ),

    path(
        "peticoes/<int:pk>/excluir/",
        views.peticao_ia_excluir,
        name="peticao_ia_excluir"
    ),

    path(
        "peticoes/<int:pk>/word/",
        views.peticao_ia_word,
        name="peticao_ia_word"
    ),

    path(
        "peticoes/<int:pk>/pdf/",
        views.peticao_ia_pdf,
        name="peticao_ia_pdf"
    ),


    path(
        "resultados/",
        views.resultados,
        name="resultados"
    ),

    path(
        "estoque/",
        views.estoque,
        name="estoque"
    ),

    path(
        "materiais/novo/",
        views.material_novo,
        name="material_novo"
    ),

    path(
        "movimentacoes/nova/",
        views.movimentacao_nova,
        name="movimentacao_nova"
    ),

    path(
        "busca/",
        views.busca_global,
        name="busca_global"
    ),
]