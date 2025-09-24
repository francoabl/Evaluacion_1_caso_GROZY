# Grozy - Sistema RAG para Optimización de Carros de Compra

## Descripción
Sistema inteligente que utiliza técnicas de RAG (Retrieval-Augmented Generation) para generar carros de compra personalizados según preferencias dietéticas y presupuesto del usuario.

## Arquitectura de la Solución

### Componentes Principales:
1. **Base de Datos de Productos**: JSON con productos scrapeados de supermercados
2. **Sistema RAG**: LangChain + FAISS para recuperación de información
3. **LLM**: GitHub Models (GPT-4o-mini) para generación de respuestas
4. **Prompts Especializados**: Plantillas optimizadas por tipo de dieta

### Flujo de Información:
```
Usuario → Consulta → RAG Retriever → Productos Relevantes → LLM → Carro Optimizado
```

## Instalación y Configuración

### Requisitos:
- Python 3.8+
- Bibliotecas: langchain, openai, faiss-cpu, python-dotenv

### Configuración:
1. Crear archivo `.env` con:
```
GITHUB_TOKEN=tu_token_aqui
OPENAI_BASE_URL=https://models.inference.ai.azure.com
```

2. Instalar dependencias:
```bash
pip install langchain langchain-openai faiss-cpu python-dotenv
```

## Ejecución

### Paso 1: Generar muestra de productos
```bash
python crear_muestra_productos.py
```

### Paso 2: Ejecutar sistema RAG
```bash
jupyter notebook Main.ipynb
```

## Casos de Uso Implementados

### 1. Dieta Vegetariana
- Excluye carnes y pescados
- Prioriza proteínas vegetales
- Balancea nutricionalmente

### 2. Dieta para Diabéticos
- Evita productos con alto azúcar
- Prioriza bajo índice glucémico
- Incluye justificación nutricional

### 3. Dieta Fitness
- Alta en proteínas
- Carbohidratos complejos
- Optimizada para rendimiento deportivo

## Estructura de Archivos
```
├── Main.ipynb              # Sistema RAG principal
├── crear_muestra_productos.py  # Script de preparación de datos
├── conexion.ipynb          # Pruebas de conexión
├── data/
│   ├── productos_unimarc.json         # Datos completos
│   └── productos_unimarc_muestra.json # Muestra para RAG
└── Informe/
    └── informe.txt         # Documentación del caso
```

## Limitaciones Conocidas
- Datos limitados a Unimarc
- Sin integración de APIs externas de nutrición
- Precios pueden estar desactualizados

## Desarrolladores
- Franco Alarcón
- Agustín Aceval

Evaluación Parcial N°1 - Ingeniería de Soluciones con IA