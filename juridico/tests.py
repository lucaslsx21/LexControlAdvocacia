from datetime import date
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Advogado, Material, MovimentacaoEstoque, PeticaoIA, Processo

class RegrasNegocioTests(TestCase):
    def setUp(self):
        self.advogado = Advogado.objects.create(nome="Ana Lima", oab="OAB/ES 12345", email="ana@example.com", data_admissao=date.today(), resumo_profissional="Experiência jurídica.")
        self.material = Material.objects.create(nome="Papel A4", categoria="Papelaria", quantidade=10, estoque_minimo=2)
    def test_numero_processo_unico(self):
        Processo.objects.create(numero="0001", titulo="Teste", area="CIVIL", advogado=self.advogado, parte_autora="A", parte_re="B", data_distribuicao=date.today())
        with self.assertRaises(Exception): Processo.objects.create(numero="0001", titulo="Outro", area="CIVIL", advogado=self.advogado, parte_autora="C", parte_re="D", data_distribuicao=date.today())
    def test_saida_atualiza_estoque(self):
        MovimentacaoEstoque.objects.create(material=self.material, tipo="SAIDA", quantidade=3)
        self.material.refresh_from_db(); self.assertEqual(self.material.quantidade, 7)
    def test_saida_maior_que_estoque_e_bloqueada(self):
        with self.assertRaises(ValidationError): MovimentacaoEstoque.objects.create(material=self.material, tipo="SAIDA", quantidade=11)
    def test_peticao_ia_inicia_como_rascunho(self):
        processo = Processo.objects.create(numero="0002", titulo="Teste IA", area="CIVIL", advogado=self.advogado, parte_autora="A", parte_re="B", data_distribuicao=date.today())
        usuario = User.objects.create_user("teste", password="senha-forte")
        peticao = PeticaoIA.objects.create(processo=processo, advogado=self.advogado, criado_por=usuario, tipo="INICIAL", objetivo="Elaborar uma minuta")
        self.assertEqual(peticao.status, "RASCUNHO")
