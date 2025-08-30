# Sistema Simplificado de Gestão de Tarefas com Relatórios

Um sistema web moderno e intuitivo para gerenciamento de tarefas pessoais ou de pequenas equipes, desenvolvido com Flask (backend) e React (frontend).

## Características Principais

### Funcionalidades Core
- ✅ **Criação de Tarefas**: Nome, prazo, anotações, status
- ✅ **Sistema de Checklist**: Subtarefas com controle individual de conclusão
- ✅ **Links Anexados**: Múltiplos links de referência por tarefa
- ✅ **Filtros e Busca**: Pesquisa por texto e filtros por status
- ✅ **Exportação de Relatórios**: Dados em formato CSV
- ✅ **Interface Responsiva**: Funciona em desktop e dispositivos móveis

### Tecnologias Utilizadas
- **Backend**: Flask, SQLAlchemy, SQLite
- **Frontend**: React, Tailwind CSS, shadcn/ui
- **Banco de Dados**: SQLite (facilmente migrável para PostgreSQL/MySQL)

## Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- Node.js 18+ (apenas para desenvolvimento do frontend)

### Instalação Rápida

1. **Clone ou baixe o projeto**
   ```bash
   # Se usando git
   git clone <repository-url>
   cd task_management_backend
   ```

2. **Configure o ambiente virtual Python**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**
   ```bash
   python src/main.py
   ```

5. **Acesse a aplicação**
   Abra seu navegador e vá para: `http://localhost:5000`

## Estrutura do Projeto

```
task_management_backend/
├── src/
│   ├── models/          # Modelos de dados (Task, ChecklistItem, TaskLink)
│   ├── routes/          # Rotas da API REST
│   ├── static/          # Arquivos do frontend (HTML, CSS, JS)
│   ├── database/        # Banco de dados SQLite
│   └── main.py          # Ponto de entrada da aplicação
├── venv/                # Ambiente virtual Python
├── requirements.txt     # Dependências Python
└── README.md           # Este arquivo
```

## API Endpoints

### Tarefas
- `GET /api/tasks` - Listar todas as tarefas
- `POST /api/tasks` - Criar nova tarefa
- `GET /api/tasks/{id}` - Obter tarefa específica
- `PUT /api/tasks/{id}` - Atualizar tarefa
- `DELETE /api/tasks/{id}` - Excluir tarefa

### Checklist
- `PATCH /api/tasks/{id}/checklist/{item_id}` - Atualizar item do checklist

### Relatórios
- `GET /api/reports/export` - Exportar tarefas em CSV

### Parâmetros de Filtro
- `status`: pending, in_progress, completed, cancelled
- `search`: busca por texto no nome ou anotações
- `format`: csv (para exportação)

## Uso da Aplicação

### Criando uma Tarefa
1. Clique em "Nova Tarefa"
2. Preencha o nome (obrigatório)
3. Defina prazo (opcional)
4. Adicione anotações (opcional)
5. Configure o status
6. Adicione itens ao checklist se necessário
7. Anexe links de referência se necessário
8. Clique em "Criar Tarefa"

### Gerenciando Tarefas
- **Buscar**: Use a caixa de busca para encontrar tarefas por nome ou conteúdo
- **Filtrar**: Use o dropdown de status para filtrar tarefas
- **Editar**: Clique no ícone de edição na tarefa
- **Excluir**: Clique no ícone de lixeira na tarefa
- **Checklist**: Marque/desmarque itens diretamente na visualização da tarefa

### Exportando Relatórios
1. Configure os filtros desejados (status, busca)
2. Clique em "Exportar"
3. O arquivo CSV será baixado automaticamente

## Modelo de Dados

### Tarefa (Task)
- ID único
- Nome (obrigatório)
- Prazo (data/hora opcional)
- Anotações (texto livre)
- Status (pending, in_progress, completed, cancelled)
- Data de criação e atualização

### Item de Checklist (ChecklistItem)
- ID único
- Referência à tarefa
- Descrição
- Status de conclusão (verdadeiro/falso)
- Ordem de exibição

### Link da Tarefa (TaskLink)
- ID único
- Referência à tarefa
- URL
- Descrição opcional

## Deployment

### Desenvolvimento Local
```bash
python src/main.py
```

### Produção
Para produção, recomenda-se usar um servidor WSGI como Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

### Docker (Opcional)
Crie um `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
EXPOSE 5000

CMD ["python", "src/main.py"]
```

## Configuração Avançada

### Banco de Dados
Por padrão, usa SQLite. Para PostgreSQL ou MySQL:

1. Instale o driver apropriado:
   ```bash
   pip install psycopg2-binary  # PostgreSQL
   # ou
   pip install pymysql          # MySQL
   ```

2. Atualize a string de conexão em `src/main.py`:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/dbname'
   ```

### Variáveis de Ambiente
Crie um arquivo `.env` para configurações:

```env
DATABASE_URL=sqlite:///database/app.db
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=False
```

## Troubleshooting

### Problemas Comuns

1. **Erro de porta em uso**
   - Altere a porta em `src/main.py` ou termine processos na porta 5000

2. **Erro de banco de dados**
   - Verifique se o diretório `src/database/` existe
   - Execute `python -c "from src.main import app; app.app_context().push(); from src.models.user import db; db.create_all()"`

3. **Problemas de CORS**
   - Verifique se `flask-cors` está instalado
   - Confirme que `CORS(app)` está configurado em `main.py`

### Logs
Para debug detalhado, defina `debug=True` em `main.py` ou use variável de ambiente `FLASK_DEBUG=1`.

## Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Suporte

Para suporte técnico ou dúvidas:
- Abra uma issue no repositório
- Consulte a documentação da API
- Verifique os logs da aplicação para diagnóstico

---

**Desenvolvido com ❤️ usando Flask e React**

