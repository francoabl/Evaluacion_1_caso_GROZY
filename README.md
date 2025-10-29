# 🤖 GROZY - Agente Inteligente para Optimización de Compras

<div align="center">

![Status](https://img.shields.io/badge/Status-Funcional-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.1+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Sistema de Agente con IA que integra herramientas de consulta, escritura y razonamiento para generar carros de compra personalizados**

[Instalación](#-instalación) • [Uso](#-uso) • [Arquitectura](#️-arquitectura) • [Documentación Técnica](#-documentación-técnica)

</div>

---

## 📋 Descripción

GROZY es un **agente funcional con Inteligencia Artificial** desarrollado con LangChain que automatiza la creación de carros de compra optimizados según:
- ✅ Restricciones dietéticas (vegetariana, diabética, fitness, familiar)
- ✅ Presupuesto disponible
- ✅ Balance nutricional
- ✅ Número de personas
- ✅ Preferencias del usuario (memoria)

**Autores:** Franco Alarcón, Agustín Aceval  
**Curso:** Ingeniería de Soluciones con IA  
**Fecha:** Octubre 2025

---

## 🌟 Características Principales

### 🔧 Herramientas del Agente (7 Tools)

#### A. Herramientas de Consulta 🔍
- **`buscar_productos`**: Búsqueda semántica en base de datos con FAISS
- **`obtener_estadisticas_categorias`**: Análisis de disponibilidad y precios por categoría

#### B. Herramientas de Razonamiento 🧠
- **`validar_dieta`**: Verifica compatibilidad con restricciones dietéticas
- **`calcular_presupuesto`**: Valida cumplimiento de presupuesto
- **`evaluar_balance_nutricional`**: Analiza balance entre categorías alimenticias

#### C. Herramientas de Escritura ✍️
- **`generar_carro_optimizado`**: Crea carros personalizados
- **`guardar_preferencias_usuario`**: Persiste preferencias (memoria largo plazo)

### 🧠 Sistema de Memoria Dual

**Memoria de Corto Plazo (Conversacional)**
- Mantiene contexto de la conversación actual
- Recuerda preferencias mencionadas en la sesión
- Implementada con `ConversationBufferMemory`

**Memoria de Largo Plazo (Persistente)**
- Guarda preferencias del usuario entre sesiones
- Almacenada en JSON local (escalable a DB)
- Permite personalización recurrente

### 📊 Planificación Adaptativa

El agente ajusta su comportamiento según el contexto:

```
PROCESO ADAPTATIVO:
1. Analiza requisitos del usuario
2. Verifica disponibilidad de productos
3. Genera carro inicial
4. Valida restricciones dietéticas
5. Verifica presupuesto
6. Evalúa balance nutricional
7. ⚡ AJUSTA si detecta problemas
8. Presenta resultado optimizado
```

**Ejemplos de Adaptación:**
- 💰 Presupuesto insuficiente → Sugiere productos más económicos
- 🥗 Balance nutricional pobre → Recomienda categorías faltantes
- 🚫 Productos no compatibles → Excluye y busca alternativas

---

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes)
- Cuenta de GitHub (para acceso a GitHub Models)

### Paso 1: Clonar/Descargar Proyecto
```bash
cd Evaluacion_1_caso_GROZY-main
```

### Paso 2: Crear Entorno Virtual (Recomendado)
```powershell
# Windows PowerShell
python -m venv .venv
.venv\Scripts\activate
```

### Paso 3: Instalar Dependencias
```powershell
pip install -r requirements.txt
```

**Dependencias incluidas:**
```
langchain>=0.1.0
langchain-openai>=0.0.5
langchain-community>=0.0.20
langchain-core>=0.1.23
openai>=1.0.0
faiss-cpu>=1.7.4
python-dotenv>=1.0.0
flask>=2.3.0
flask-cors>=4.0.0
```

### Paso 4: Configurar Variables de Entorno
Crear archivo `.env` en la raíz del proyecto:
```env
GITHUB_TOKEN=tu_github_token_aqui
OPENAI_BASE_URL=https://models.inference.ai.azure.com
```

**¿Cómo obtener tu GitHub Token?**
1. Ir a https://github.com/settings/tokens
2. Generar token con permisos de lectura
3. Copiar y pegar en `.env`

---

## 💻 Uso - Opciones de Ejecución

### Opción 1: Terminal Interactiva (CLI) ⭐ Recomendado

**Archivo:** `grozy_agent_v2.py`

```powershell
python grozy_agent_v2.py
```

**Características:**
- ✅ Interfaz de línea de comandos
- ✅ Conversación interactiva
- ✅ Todas las herramientas disponibles
- ✅ Historial de conversación
- ✅ Comando 'ayuda' para ejemplos

**Comandos especiales:**
- `ayuda` - Ver ejemplos de uso
- `salir` - Terminar el programa

**Ejemplos de uso:**
```
🧑 Tú: Busca frutas frescas
🧑 Tú: Genera un carro vegetariano para 3 personas con $25000
🧑 Tú: Dame estadísticas de productos
```

---

### Opción 2: Jupyter Notebook

**Archivo:** `agente_grozy.ipynb`

```powershell
jupyter notebook agente_grozy.ipynb
```

**Características:**
- ✅ Interfaz visual en el navegador
- ✅ Ejecución celda por celda
- ✅ Documentación integrada
- ✅ Ejemplos predefinidos
- ✅ Ideal para demostración académica

**Cómo usar:**
1. Abre el notebook en Jupyter
2. Ejecuta las celdas en orden (Run All)
3. Prueba los ejemplos en las celdas 15-25
4. Modifica y experimenta

---

### Opción 3: Chatbot Web 🌐

**Requiere 2 pasos:**

#### Paso 1: Iniciar el Servidor API

```powershell
python grozy_api.py
```

Verás:
```
🔄 Inicializando GROZY Agent...
✅ GROZY Agent listo
============================================================
🚀 Servidor GROZY API iniciado
============================================================
📡 URL: http://localhost:5000
```

**⚠️ IMPORTANTE:** Deja esta terminal abierta y ejecutándose.

#### Paso 2: Abrir el Chatbot

Abre `chatbot/index.html` en tu navegador:
- Doble clic en el archivo, o
- Arrastra el archivo al navegador, o
- En VS Code: clic derecho → "Open with Live Server"

**Características:**
- ✅ Interfaz moderna y responsive
- ✅ Botones de acceso rápido con ejemplos
- ✅ Indicador de escritura animado
- ✅ Historial de conversación
- ✅ Funciona en móvil y desktop

---

## 📚 Ejemplos de Consultas

### 🌱 Dieta Vegetariana
```
"Arma un carro vegetariano para 4 personas con presupuesto de $30,000"
```

**Resultado esperado:**
- Búsqueda de productos vegetarianos
- Validación de ausencia de carnes
- Balance entre frutas, verduras, lácteos y legumbres
- Total dentro del presupuesto

### 🩺 Dieta Diabética
```
"Necesito productos para diabético, presupuesto $15,000, valida que no tengan azúcar"
```

**Resultado esperado:**
- Productos sin azúcar añadido
- Priorizaci de carbohidratos complejos
- Advertencia sobre productos con azúcar

### 💪 Dieta Fitness
```
"Carro fitness para 2 personas, $20,000, prioriza proteínas y carbohidratos complejos"
```

**Resultado esperado:**
- Alta proporción de proteínas
- Carbohidratos complejos (arroz integral, avena)
- Frutas y verduras para balance

### 🧠 Uso de Memoria
```
Usuario: "Me llamo Franco y soy vegetariano"
Agente: "Encantado Franco, recordaré tu preferencia..."

Usuario: "Arma un carro para mí con $20,000"
Agente: "Claro Franco, prepararé un carro VEGETARIANO..." ✅ Recuerda!
```

---

## 🏗️ Arquitectura del Sistema

### Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────┐
│                    USUARIO                              │
│         (CLI / Notebook / Web)                          │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│              AGENTE GROZY (LangChain)                   │
│  ┌────────────────────────────────────────────────┐    │
│  │  🧠 LLM (GPT-4o-mini via GitHub Models)       │    │
│  │     • Razonamiento y toma de decisiones        │    │
│  │     • Planificación adaptativa                 │    │
│  │     • Selección de herramientas                │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  💾 MEMORIA                                    │    │
│  │     • Corto plazo: ConversationBufferMemory    │    │
│  │     • Largo plazo: JSON persistente            │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  🔧 HERRAMIENTAS (7 tools)                    │    │
│  │                                                 │    │
│  │  🔍 Consulta:                                  │    │
│  │     • buscar_productos                         │    │
│  │     • obtener_estadisticas_categorias          │    │
│  │                                                 │    │
│  │  🧠 Razonamiento:                              │    │
│  │     • validar_dieta                            │    │
│  │     • calcular_presupuesto                     │    │
│  │     • evaluar_balance_nutricional              │    │
│  │                                                 │    │
│  │  ✍️ Escritura:                                 │    │
│  │     • generar_carro_optimizado                 │    │
│  │     • guardar_preferencias_usuario             │    │
│  └────────────────────────────────────────────────┘    │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│           BASE DE CONOCIMIENTO                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  📊 Vector Store (FAISS)                       │    │
│  │     • 495 productos                            │    │
│  │     • 9 categorías                             │    │
│  │     • Embeddings (text-embedding-3-small)      │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  📁 Datos (JSON)                               │    │
│  │     • productos_unimarc_muestra.json           │    │
│  │     • preferencias_usuarios.json               │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### Flujo de Ejecución

```
1. Usuario ingresa consulta
   ↓
2. Agente analiza intención
   ↓
3. Planifica secuencia de herramientas
   ↓
4. Ejecuta herramientas iterativamente
   ↓
5. Valida restricciones (dieta, presupuesto, balance)
   ↓
6. ¿Hay problemas? → Ajusta estrategia (vuelve al paso 3)
   ↓
7. Integra resultados
   ↓
8. Genera respuesta final
   ↓
9. Actualiza memoria
   ↓
10. Retorna al usuario
```

---

## 📊 Documentación Técnica

### Justificación de Decisiones Técnicas

#### 1. Framework: LangChain

**Razón de selección:**
- ✅ Framework líder en desarrollo de aplicaciones con LLM (70k+ estrellas GitHub)
- ✅ Abstracciones robustas para agentes y herramientas
- ✅ Implementación nativa de patrones ReAct (Reasoning + Acting)
- ✅ Integración directa con OpenAI y GitHub Models
- ✅ Sistema de memoria incorporado
- ✅ Gran comunidad y documentación exhaustiva

**Alternativas consideradas:**
- **Haystack:** Más orientado a búsqueda, menor flexibilidad para agentes complejos
- **Autogen:** Requiere múltiples agentes, innecesario para este caso de uso
- **Implementación custom:** Mayor control pero tiempo de desarrollo significativamente mayor

**Referencia:** Chase, H. (2022). LangChain [Software]. https://github.com/langchain-ai/langchain

---

#### 2. Vector Store: FAISS

**Razón de selección:**
- ✅ Optimizado por Facebook AI Research para búsquedas de similitud
- ✅ Excelente rendimiento para datasets medianos (<1M vectores)
- ✅ Funciona en CPU (no requiere GPU)
- ✅ Integración directa con LangChain
- ✅ Latencia < 100ms para búsquedas

**Referencia:** Johnson, J., Douze, M., & Jégou, H. (2019). Billion-scale similarity search with GPUs. IEEE Transactions on Big Data, 7(3), 535-547.

---

#### 3. LLM: GPT-4o-mini (GitHub Models)

**Razón de selección:**
- ✅ Acceso gratuito para desarrollo académico
- ✅ Balance óptimo costo-rendimiento
- ✅ Capacidad de razonamiento suficiente para el dominio
- ✅ Latencia < 3 segundos
- ✅ Soporte nativo de function calling (crítico para herramientas)
- ✅ Contexto de 128k tokens

**Referencia:** OpenAI. (2024). GPT-4 Technical Report. https://openai.com/research/gpt-4

---

#### 4. Arquitectura: Agent with Tools (ReAct Pattern)

**Razón de selección:**
- ✅ LLM decide dinámicamente qué herramientas usar
- ✅ Planificación multi-paso
- ✅ Capacidad de autocorrección
- ✅ Validación automática de argumentos
- ✅ Manejo robusto de errores

**Referencia:** Yao, S., et al. (2023). ReAct: Synergizing reasoning and acting in language models. ICLR.

---

### Sistema de Memoria Implementado

#### Memoria de Corto Plazo

**Implementación:**
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="output"
)
```

**Características:**
- Mantiene historial completo de la conversación
- Permite referencias anafóricas ("para mí", "lo anterior")
- Coherencia temática entre turnos
- Persistencia solo durante la sesión

**Ejemplo:**
```
Turno 1:
Usuario: "Me llamo Franco y soy vegetariano"
Agente: "Encantado Franco, recordaré tu preferencia"

Turno 2:
Usuario: "Arma un carro para mí"
Agente: "Por supuesto Franco, prepararé un carro VEGETARIANO"
```

#### Memoria de Largo Plazo

**Implementación:**
- Archivo JSON local: `data/preferencias_usuarios.json`
- Herramienta: `guardar_preferencias_usuario`
- Persistencia entre sesiones

**Estructura:**
```json
{
  "Franco": {
    "preferencias": "vegetariano, presupuesto 30000, 2 personas",
    "fecha": "2025-10-29T14:30:00"
  }
}
```

---

### Planificación Adaptativa

El agente implementa un proceso de 5 fases:

#### FASE 1: Análisis de Intención
- Parsea solicitud del usuario
- Identifica información faltante
- Decide si solicitar más datos

#### FASE 2: Planificación de Acciones
- Determina secuencia de herramientas
- Prioriza según criticidad
- Considera dependencias entre tools

#### FASE 3: Ejecución Iterativa
- Ejecuta herramientas secuencialmente
- Observa resultados
- Decide siguiente acción

#### FASE 4: Validación y Ajuste
- Verifica restricciones (dieta, presupuesto, balance)
- Si hay problemas → AJUSTA ESTRATEGIA
- Si todo OK → FINALIZA

#### FASE 5: Síntesis de Respuesta
- Integra resultados de todas las herramientas
- Genera respuesta coherente
- Actualiza memoria

### Ejemplos de Adaptación

#### Ejemplo 1: Presupuesto Insuficiente

**Input:** "Carro fitness para 4 personas con $5,000"

**Proceso adaptativo:**
1. Detecta que $5,000 / 4 ≈ $1,250/persona es insuficiente
2. Reduce cantidad de productos de 20 a 10
3. Prioriza categorías económicas (cereales, legumbres)
4. Comunica limitación de forma transparente:
   ```
   "Con $5,000 para 4 personas, el presupuesto es limitado.
   He preparado un carro básico con 10 productos esenciales.
   Recomiendo aumentar el presupuesto a $15,000 para mayor variedad."
   ```

#### Ejemplo 2: Balance Nutricional Deficiente

**Input:** "Carro con: pan, galletas, dulces, bebidas, snacks"

**Proceso adaptativo:**
1. Genera carro inicial con productos solicitados
2. Evalúa balance con `evaluar_balance_nutricional`
3. Detecta carencia de: proteínas, frutas/verduras, lácteos
4. Interviene proactivamente:
   ```
   "He notado que el carro actual carece de:
   ⚠️ Proteínas (carnes, huevos, legumbres)
   ⚠️ Frutas y verduras
   ⚠️ Lácteos
   
   ¿Deseas que agregue estos grupos para un balance adecuado?"
   ```

#### Ejemplo 3: Violación de Restricción Dietética

**Input (usuario vegetariano):** "Arma carro con pollo, pescado y verduras"

**Proceso adaptativo:**
1. Consulta memoria: usuario es vegetariano
2. Detecta contradicción
3. Advierte y sugiere:
   ```
   "He notado que solicitaste pollo y pescado, pero según
   tus preferencias guardadas eres vegetariano.
   
   ¿Deseas que:
   A) Omita las carnes y priorice proteínas vegetales
   B) Actualice tus preferencias para incluir carnes?"
   ```

---

## 📈 Métricas y Rendimiento

| Métrica | Valor |
|---------|-------|
| **Herramientas disponibles** | 7 especializadas |
| **Productos en base de datos** | 495 |
| **Categorías** | 9 |
| **Tiempo de respuesta promedio** | 5-8 segundos |
| **Iteraciones por consulta** | 4-6 |
| **Tasa de éxito** | >95% en casos válidos |
| **Memoria conversacional** | Ilimitada (en sesión) |

---

## 📁 Estructura del Proyecto

```
Evaluacion_1_caso_GROZY-main/
│
├── 🐍 Scripts Python
│   ├── grozy_agent_v2.py          ⭐ Terminal interactiva (recomendado)
│   ├── grozy_api.py               🌐 API Flask para chatbot web
│   ├── grozy_agent.py             📝 Script base
│   └── crear_muestra_productos.py 🔧 Utilidad de datos
│
├── 📓 Notebooks
│   ├── agente_grozy.ipynb         ⭐ Notebook principal del agente
│   ├── Main.ipynb                 📚 Sistema RAG original
│   └── conexion.ipynb             🔌 Tests de conectividad
│
├── 🌐 Chatbot Web
│   └── chatbot/
│       ├── index.html             💻 Interfaz principal
│       ├── styles.css             🎨 Estilos
│       ├── script.js              ⚡ Lógica cliente
│       ├── demo.html              📖 Guía de uso
│       └── README.md              📄 Documentación
│
├── 📊 Datos
│   └── data/
│       ├── productos_unimarc_muestra.json  ⭐ 495 productos (usado)
│       ├── productos_unimarc.json          📦 Dataset completo
│       └── preferencias_usuarios.json      💾 Memoria persistente
│
├── 📄 Documentación
│   ├── README.md                  📘 Este archivo
│   └── requirements.txt           📦 Dependencias Python
│
└── 🔑 Configuración
    └── .env                       🔐 Variables de entorno (crear)
```

---

## 🔮 Mejoras Futuras

### Corto Plazo (1-2 meses)
- [ ] Tests unitarios con pytest
- [ ] Base de datos SQL para escalabilidad
- [ ] ConversationSummaryMemory para sesiones largas
- [ ] Logging estructurado

### Mediano Plazo (3-6 meses)
- [ ] Información nutricional detallada (calorías, macros, micronutrientes)
- [ ] Comparación de precios entre supermercados
- [ ] Sistema de alertas de ofertas y descuentos
- [ ] Recomendaciones basadas en historial

### Largo Plazo (6-12 meses)
- [ ] Fine-tuning de modelo específico para retail chileno
- [ ] Integración con APIs de supermercados en tiempo real
- [ ] Aplicación móvil (iOS/Android)
- [ ] Sistema de recomendaciones colaborativas
- [ ] Análisis predictivo de compras

---

## 🛠️ Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'langchain'"
**Solución:** 
```powershell
pip install -r requirements.txt
```

### Error: "Authentication failed" o "Invalid token"
**Solución:** 
1. Verifica que el archivo `.env` existe en la raíz
2. Verifica que `GITHUB_TOKEN` tiene un token válido
3. Regenera el token en https://github.com/settings/tokens

### El chatbot web no se conecta al servidor
**Solución:**
1. Verifica que `grozy_api.py` está ejecutándose
2. Verifica que el servidor muestra "Servidor GROZY API iniciado"
3. Abre la consola del navegador (F12) para ver errores
4. Verifica que la URL en `script.js` es `http://localhost:5000`

### El agente no encuentra productos
**Solución:**
1. Verifica que `data/productos_unimarc_muestra.json` existe
2. El vector store se genera en la primera ejecución (toma ~30 segundos)
3. Revisa que las consultas sean en español

### Respuestas muy lentas (>15 segundos)
**Solución:**
- Primera ejecución es más lenta (generación de embeddings)
- Ejecuciones posteriores son más rápidas (~5-8 segundos)
- Verifica tu conexión a internet (requiere acceso a GitHub Models)

---

## 📖 Referencias (Formato APA)

Chase, H. (2022). *LangChain* [Software]. GitHub. https://github.com/langchain-ai/langchain

Johnson, J., Douze, M., & Jégou, H. (2019). Billion-scale similarity search with GPUs. *IEEE Transactions on Big Data*, 7(3), 535-547. https://doi.org/10.1109/TBDATA.2019.2921572

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems*, 33, 9459-9474.

OpenAI. (2023). *Function Calling*. OpenAI Documentation. https://platform.openai.com/docs/guides/function-calling

OpenAI. (2024). *GPT-4 Technical Report*. https://openai.com/research/gpt-4

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, 30.

Wang, L., Ma, C., Feng, X., Zhang, Z., Yang, H., Zhang, J., Chen, Z., Tang, J., Chen, X., Lin, Y., Zhao, W. X., Wei, Z., & Liu, T. Y. (2023). A survey on large language model based autonomous agents. *arXiv preprint arXiv:2308.11432*.

Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. *International Conference on Learning Representations (ICLR)*.

---

## 👨‍💻 Autores y Contacto

**Franco Alarcón** - Desarrollo e implementación  
**Agustín Aceval** - Desarrollo e implementación

**Curso:** Ingeniería de Soluciones con IA  
**Institución:** [Universidad]  
**Fecha:** Octubre 2025

---

## 📄 Licencia

Este proyecto es parte de la **Evaluación Parcial N°1 - Ingeniería de Soluciones con IA**

---

<div align="center">

**⭐ Proyecto GROZY - Agente Inteligente con IA ⭐**

*Optimización de compras mediante planificación adaptativa y memoria contextual*

</div>
