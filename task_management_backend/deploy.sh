#!/bin/bash

# Sistema de Gestão de Tarefas - Script de Deploy
echo "=== Sistema de Gestão de Tarefas - Deploy ==="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.11 ou superior."
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt

# Verificar se banco de dados existe, se não, criar
if [ ! -f "src/database/app.db" ]; then
    echo "🗄️ Criando banco de dados..."
    mkdir -p src/database
    python3 -c "
from src.main import app
with app.app_context():
    from src.models.user import db
    from src.models.task import Task, ChecklistItem, TaskLink
    db.create_all()
    print('Banco de dados criado com sucesso!')
"
fi

echo ""
echo "🎉 Deploy concluído com sucesso!"
echo ""
echo "Para iniciar a aplicação, execute:"
echo "  source venv/bin/activate"
echo "  python src/main.py"
echo ""
echo "Depois acesse: http://localhost:5000"
echo ""

