from django import forms
from .models import Advogado, Andamento, HistoricoAdvogado, Material, MovimentacaoEstoque, PeticaoIA, Processo

class FormBase(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

class AdvogadoForm(FormBase):
    class Meta:
        model = Advogado
        fields = "__all__"
        widgets = {"data_admissao": forms.DateInput(attrs={"type": "date"}), "resumo_profissional": forms.Textarea(attrs={"rows": 4})}

class HistoricoForm(FormBase):
    class Meta:
        model = HistoricoAdvogado
        fields = "__all__"
        widgets = {"data_evento": forms.DateTimeInput(attrs={"type": "datetime-local"})}

class ProcessoForm(FormBase):
    class Meta:
        model = Processo
        fields = "__all__"
        widgets = {"data_distribuicao": forms.DateInput(attrs={"type": "date"}), "prazo_atual": forms.DateTimeInput(attrs={"type": "datetime-local"})}

class AndamentoForm(FormBase):

    class Meta:
        model = Andamento

        fields = [
            "processo",
            "data",
            "descricao",
            "responsavel",
            "status_processo",
        ]

        widgets = {
            "data": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local"
                }
            ),

            "descricao": forms.Textarea(
                attrs={
                    "rows": 5
                }
            ),
        }

class MaterialForm(FormBase):
    class Meta: model = Material; fields = "__all__"

class MovimentacaoForm(FormBase):
    class Meta: model = MovimentacaoEstoque; fields = ["material", "tipo", "quantidade", "observacao"]

class ImportarProcessoForm(forms.Form):
    arquivo = forms.FileField(help_text="Formatos aceitos: PDF pesquisável, DOCX ou TXT (máximo de 50 MB).")
    advogado = forms.ModelChoiceField(queryset=Advogado.objects.filter(ativo=True), required=False, help_text="Opcional. O sistema tentará localizar o advogado no documento.")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values(): field.widget.attrs["class"] = "form-control"
    def clean_arquivo(self):
        arquivo = self.cleaned_data["arquivo"]
        if arquivo.size > 50 * 1024 * 1024: raise forms.ValidationError("O arquivo deve ter no máximo 50 MB.")
        if not arquivo.name.lower().endswith((".pdf", ".docx", ".txt")): raise forms.ValidationError("Envie um arquivo PDF, DOCX ou TXT.")
        return arquivo

class PeticaoIAForm(FormBase):
    usar_documentos = forms.BooleanField(required=False, initial=True, label="Utilizar documentos anexados ao processo")
    confirmacao_revisao = forms.BooleanField(required=True, label="Estou ciente de que a minuta deverá ser revisada por um advogado.")
    class Meta:
        model = PeticaoIA
        fields = ["tipo", "objetivo", "fatos_complementares", "fundamentos_sugeridos", "pedidos_especificos", "orientacoes"]
        widgets = {
            "objetivo": forms.Textarea(attrs={"rows": 4}),
            "fatos_complementares": forms.Textarea(attrs={"rows": 5}),
            "fundamentos_sugeridos": forms.Textarea(attrs={"rows": 4}),
            "pedidos_especificos": forms.Textarea(attrs={"rows": 4}),
            "orientacoes": forms.Textarea(attrs={"rows": 3}),
        }

class RevisarPeticaoForm(FormBase):
    class Meta:
        model = PeticaoIA
        fields = ["texto_gerado", "status"]
        widgets = {"texto_gerado": forms.Textarea(attrs={"rows": 35, "class": "form-control editor-peticao"})}
