#!/bin/bash

# Script de verificación del proyecto AWS Cost Optimizer AI
# Verifica que todos los archivos necesarios existen y el proyecto funciona

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║           AWS COST OPTIMIZER AI - VERIFICACIÓN DEL PROYECTO                 ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador de errores
ERRORS=0

# Función para verificar archivo
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅${NC} $1"
    else
        echo -e "${RED}❌${NC} $1 - NO ENCONTRADO"
        ((ERRORS++))
    fi
}

# Función para verificar directorio
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅${NC} $1/"
    else
        echo -e "${RED}❌${NC} $1/ - NO ENCONTRADO"
        ((ERRORS++))
    fi
}

echo "📁 Verificando estructura de directorios..."
echo ""
check_dir "src"
check_dir "data"
check_dir "templates"
check_dir "terraform"
check_dir "docs"
check_dir ".github/workflows"

echo ""
echo "📄 Verificando archivos principales..."
echo ""
check_file "README.md"
check_file "README_MALT.md"
check_file "LICENSE"
check_file "requirements.txt"
check_file ".env.example"
check_file ".gitignore"
check_file "SETUP.md"
check_file "CONTRIBUTING.md"
check_file "INSTRUCCIONES_GITHUB.md"
check_file "RESUMEN_PROYECTO.md"

echo ""
echo "🐍 Verificando archivos Python..."
echo ""
check_file "src/__init__.py"
check_file "src/main.py"
check_file "src/cost_analyzer.py"
check_file "src/bedrock_analyzer.py"
check_file "src/recommendations.py"
check_file "src/dashboard.py"

echo ""
echo "📊 Verificando datos y templates..."
echo ""
check_file "data/sample_cost_data.json"

echo ""
echo "🏗️ Verificando Terraform..."
echo ""
check_file "terraform/main.tf"
check_file "terraform/variables.tf"
check_file "terraform/outputs.tf"

echo ""
echo "🔄 Verificando CI/CD..."
echo ""
check_file ".github/workflows/ci-cd.yml"

echo ""
echo "📚 Verificando documentación..."
echo ""
check_file "docs/architecture.md"

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ VERIFICACIÓN EXITOSA${NC}"
    echo "Todos los archivos necesarios están presentes."
    echo ""
    echo "🚀 Siguiente paso: Probar el proyecto"
    echo ""
    echo "Ejecuta:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo "  python src/main.py --demo"
    echo ""
else
    echo -e "${RED}❌ VERIFICACIÓN FALLIDA${NC}"
    echo "Faltan $ERRORS archivo(s)."
    echo ""
    echo "Por favor, verifica que todos los archivos se hayan creado correctamente."
fi

echo "════════════════════════════════════════════════════════════════════════════════"
