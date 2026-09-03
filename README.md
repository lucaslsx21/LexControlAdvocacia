# LexControl IA — Plataforma Web para Escritório de Advocacia

Sistema criado em Python com Django, banco SQLite e interface responsiva. Inclui login, advogados/OAB, histórico, processos, busca global, andamento, estoque, importação de documentos e um Assistente de Petições com OpenAI. A IA usa os dados do processo, cria uma minuta, exige revisão humana e permite exportação em Word/PDF.

## 1. Preparação do ambiente (Windows/PowerShell)

```powershell
cd plataforma_advocacia
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 1.1 Configurar a inteligência artificial

Crie sua chave no painel da API da OpenAI. Copie `.env.example` para `.env`:

```powershell
Copy-Item .env.example .env
```

Abra `.env` e substitua o valor de `OPENAI_API_KEY`. Nunca envie esse arquivo ao GitHub. O ChatGPT Plus e a API possuem cobranças separadas; a API precisa estar habilitada no projeto da OpenAI.

Se o PowerShell bloquear a ativação, execute uma vez: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## 2. Banco de dados e primeiro usuário

```powershell
python manage.py makemigrations juridico
python manage.py migrate
python manage.py createsuperuser
```

O `makemigrations` transforma os modelos Python em uma migração; o `migrate` cria as tabelas; o `createsuperuser` cria o usuário que acessará `/login/` e `/admin/`.

## 3. Executar

```powershell
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/login/`.

## 4. Como o projeto está organizado

- `config/settings.py`: banco, idioma, fuso horário, apps e arquivos estáticos.
- `config/urls.py`: rotas gerais, autenticação e painel administrativo.
- `juridico/models.py`: estrutura das tabelas e regras de negócio.
- `juridico/forms.py`: formulários de cadastro e edição.
- `juridico/views.py`: consultas, filtros, busca e geração de relatórios.
- `juridico/urls.py`: endereços de cada tela.
- `templates/`: HTML compartilhado e páginas do sistema.
- `static/css/style.css`: aparência responsiva inspirada no modelo anexado.
- `juridico/tests.py`: testes automatizados das regras críticas.

## 5. Modelagem explicada

### Advogado e histórico

`Advogado` guarda nome, OAB única, contatos, admissão, formação, especialidades e resumo. `HistoricoAdvogado` possui chave estrangeira para o advogado e forma uma linha do tempo com data/hora, título e descrição.

### Processo e andamento

`Processo` possui número único, partes, advogado responsável, tribunal, comarca, valor, prazo e uma das áreas: Penal, Tributário, Trabalho, Civil, Família ou Consumidor. Os status incluem Novo, Em andamento, Deferido, Indeferido, Suspenso e Concluído. `Andamento` registra uma linha do tempo para cada processo.

### Estoque

`Material` guarda saldo e estoque mínimo. `MovimentacaoEstoque` registra entrada/saída, data/hora e observação. O método `clean()` bloqueia saída superior ao saldo; o `save()` atualiza o saldo somente ao criar a movimentação.

## 6. Pesquisa global

A barra superior envia o termo para `busca_global`. A view usa objetos `Q` e `icontains`, pesquisando simultaneamente nos processos (número, título, partes, descrição e tribunal), advogados (nome, OAB e histórico), materiais e andamentos. Os filtros específicos de processos podem ser combinados com área e status.

## 7. PDF e Word

A view `exportar` recebe o módulo e o formato. Para Word usa `python-docx`; para PDF usa `ReportLab`. Os relatórios registram a data e hora de geração e podem ser baixados nas telas de Advogados, Processos e Estoque.

## 7.1 Anexar e importar um processo

Na tela Processos, clique em **Anexar e importar**. O sistema aceita PDF pesquisável, DOCX e TXT de até 15 MB. `services.py` extrai o texto e procura número CNJ, classe/assunto, área jurídica, status, partes, advogado pelo nome/OAB, tribunal, comarca, datas, prazo e valor da causa. O processo é criado automaticamente e o arquivo fica ligado a ele.

O advogado pode ser selecionado no envio quando não estiver escrito no documento. Número, parte autora, parte ré e advogado são obrigatórios; se algum deles não for identificado, o sistema informa exatamente o que faltou, sem criar um cadastro incompleto. PDF composto apenas por imagem precisa passar por OCR e não é processado nesta versão.

## 7.2 Exclusão segura

Os botões vermelhos nas listas abrem uma confirmação. A exclusão de processo remove também seus andamentos e documentos. Um advogado com processos vinculados não pode ser excluído até que esses processos sejam transferidos para outro advogado ou removidos.

## 8. Testar

```powershell
python manage.py check
python manage.py test
```

Os testes verificam unicidade do processo, atualização de estoque e bloqueio de saldo negativo.

## 9. Fluxo recomendado de uso

1. Entre com o superusuário.
2. Cadastre os advogados e suas matrículas da OAB.
3. Adicione eventos no histórico profissional.
4. Cadastre manualmente ou importe processos por PDF, DOCX ou TXT.
5. Abra o processo e clique em **Criar petição com IA**.
6. Escolha o tipo da peça, informe objetivo, fatos, fundamentos e pedidos.
7. Revise a minuta e somente então marque como aprovada.
8. Exporte a peça para Word ou PDF.
9. Registre os andamentos e atualize o status.
10. Use os demais módulos normalmente.

## 9.1 Segurança jurídica e privacidade

- A IA produz somente uma minuta e não protocola documentos.
- O prompt impede invenção de fatos, artigos e jurisprudência e inclui marcadores quando faltam informações.
- A requisição usa `store=False`, mas o escritório deve avaliar contrato, retenção, sigilo profissional e LGPD antes de enviar dados reais.
- Dados pessoais sensíveis devem ser minimizados ou anonimizados quando possível.
- A chave da API fica somente no servidor.
- Para produção, use PostgreSQL, HTTPS, permissões por perfil, trilha de auditoria e tarefas em segundo plano.

## 10. Produção e segurança

Antes de publicar: mova `SECRET_KEY` para variável de ambiente; defina `DEBUG=False`; configure `ALLOWED_HOSTS`; use PostgreSQL; ative HTTPS; implemente backups e perfis de permissão. Como o sistema pode armazenar dados jurídicos e pessoais, aplique controle de acesso, registro de auditoria, política de retenção e medidas compatíveis com a LGPD. O projeto é uma base funcional e deve passar por revisão técnica e jurídica antes do uso real.
