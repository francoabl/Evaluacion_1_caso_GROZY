"""
GROZY Agent - Sistema Inteligente de Optimización de Compras
Versión funcional usando LangChain 1.0+ con create_agent
"""

import json
import os
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

# LangChain Core
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage

# LangChain para Agentes (API de LangChain 1.0+)
from langchain.agents import create_agent

# Cargar variables de entorno
load_dotenv()

print("="*60)
print("🤖 GROZY - Sistema Inteligente de Optimización de Compras")
print("="*60)
print(f"📅 Sesión iniciada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# ============================================================================
# CONFIGURACIÓN Y CARGA DE DATOS
# ============================================================================

# Configuración de credenciales
github_token = os.getenv('GITHUB_TOKEN')
openai_base_url = os.getenv('OPENAI_BASE_URL')

if not github_token:
    print("❌ Error: GITHUB_TOKEN no está configurado")
    raise ValueError("Configura GITHUB_TOKEN en el archivo .env")

print("✅ Credenciales configuradas")

# Cargar productos
file_path = os.path.join("data", "productos_unimarc_muestra.json")
with open(file_path, "r", encoding="utf-8") as f:
    productos = json.load(f)

print(f"✅ Cargados {len(productos)} productos")

# Convertir a documentos con metadata enriquecida
docs = []
for p in productos:
    contenido = (
        f"Nombre: {p['nombre']} | "
        f"Precio: ${p['precio']} | "
        f"Categoría: {p['categoria']} | "
        f"Subcategoría: {p.get('subcategoria', 'N/A')} | "
        f"Supermercado: {p['supermercado']}"
    )
    docs.append(Document(
        page_content=contenido,
        metadata={
            "nombre": p['nombre'],
            "precio": p['precio'],
            "categoria": p['categoria'],
            "subcategoria": p.get('subcategoria', 'N/A'),
            "supermercado": p['supermercado']
        }
    ))

# Crear embeddings y vector store
embeddings = OpenAIEmbeddings(
    api_key=github_token,
    base_url=openai_base_url,
    model="text-embedding-3-small"
)

print("🔄 Creando vector store (puede tardar)...")
vectorstore = FAISS.from_documents(docs, embeddings)
print("✅ Vector store creado exitosamente")

# Configurar LLM
llm = ChatOpenAI(
    api_key=github_token,
    base_url=openai_base_url,
    model="gpt-4o-mini",
    temperature=0.7
)
print("✅ LLM configurado (gpt-4o-mini)")
print()

# ============================================================================
# DEFINICIÓN DE HERRAMIENTAS
# ============================================================================

# --- Herramientas de Consulta ---

@tool
def buscar_productos(query: str, k: int = 10) -> str:
    """Busca productos en la base de datos usando búsqueda semántica.
    
    Args:
        query: Descripción de los productos a buscar (ej: 'frutas frescas', 'lácteos bajos en grasa')
        k: Número máximo de productos a retornar (default: 10)
    
    Returns:
        Lista de productos encontrados con nombre, precio y categoría
    """
    results = vectorstore.similarity_search(query, k=k)
    productos_encontrados = []
    
    for doc in results:
        productos_encontrados.append(
            f"- {doc.metadata['nombre']} | ${doc.metadata['precio']} | {doc.metadata['categoria']}"
        )
    
    return f"Productos encontrados ({len(productos_encontrados)}):\n" + "\n".join(productos_encontrados)


@tool
def obtener_estadisticas_categorias() -> str:
    """Obtiene estadísticas de productos por categoría y precios promedio.
    
    Returns:
        Resumen estadístico de categorías disponibles
    """
    categorias = {}
    precios_por_cat = {}
    
    for p in productos:
        cat = p['categoria']
        categorias[cat] = categorias.get(cat, 0) + 1
        if cat not in precios_por_cat:
            precios_por_cat[cat] = []
        precios_por_cat[cat].append(p['precio'])
    
    resultado = "📊 ESTADÍSTICAS DE PRODUCTOS:\n\n"
    resultado += f"Total productos: {len(productos)}\n"
    resultado += f"Categorías: {len(categorias)}\n\n"
    resultado += "Por categoría:\n"
    
    for cat, count in sorted(categorias.items(), key=lambda x: x[1], reverse=True)[:8]:
        precio_prom = sum(precios_por_cat[cat]) / len(precios_por_cat[cat])
        resultado += f"  • {cat}: {count} productos (promedio ${precio_prom:,.0f})\n"
    
    return resultado


# --- Herramientas de Razonamiento ---

@tool
def validar_dieta(productos_seleccionados: str, tipo_dieta: str) -> str:
    """Valida si los productos seleccionados cumplen con restricciones dietéticas.
    
    Args:
        productos_seleccionados: Lista de nombres de productos separados por coma
        tipo_dieta: Tipo de dieta ('vegetariana', 'diabetica', 'fitness', 'celiaca')
    
    Returns:
        Análisis de compatibilidad con la dieta
    """
    productos_lista = [p.strip() for p in productos_seleccionados.split(',')]
    
    restricciones = {
        'vegetariana': ['carne', 'pollo', 'pavo', 'pescado', 'atun', 'salmon', 'cerdo'],
        'diabetica': ['azucar', 'dulce', 'chocolate', 'caramelo', 'bebida', 'jugo'],
        'fitness': [],  # Sin restricciones específicas
        'celiaca': ['pan', 'trigo', 'harina', 'pasta', 'galleta']
    }
    
    palabras_prohibidas = restricciones.get(tipo_dieta.lower(), [])
    problemas = []
    
    for producto in productos_lista:
        for palabra in palabras_prohibidas:
            if palabra in producto.lower():
                problemas.append(f"⚠️ '{producto}' contiene '{palabra}' (no compatible con dieta {tipo_dieta})")
    
    if not problemas:
        return f"✅ Todos los productos son compatibles con la dieta {tipo_dieta}"
    else:
        return "Problemas encontrados:\n" + "\n".join(problemas)


@tool
def calcular_presupuesto(productos_seleccionados: str, presupuesto_max: float) -> str:
    """Calcula el costo total y verifica si está dentro del presupuesto.
    
    Args:
        productos_seleccionados: Lista de nombres de productos separados por coma
        presupuesto_max: Presupuesto máximo disponible en CLP
    
    Returns:
        Análisis de costos y cumplimiento de presupuesto
    """
    productos_lista = [p.strip().lower() for p in productos_seleccionados.split(',')]
    total = 0
    productos_con_precio = []
    
    for nombre_prod in productos_lista:
        encontrado = False
        for p in productos:
            if nombre_prod in p['nombre'].lower():
                total += p['precio']
                productos_con_precio.append(f"  • {p['nombre']}: ${p['precio']:,}")
                encontrado = True
                break
        
        if not encontrado:
            productos_con_precio.append(f"  • {nombre_prod}: ⚠️ No encontrado")
    
    resultado = "💰 ANÁLISIS DE PRESUPUESTO:\n\n"
    resultado += "\n".join(productos_con_precio)
    resultado += f"\n\nTotal: ${total:,} CLP\n"
    resultado += f"Presupuesto máximo: ${presupuesto_max:,} CLP\n"
    
    if total <= presupuesto_max:
        resultado += f"✅ Dentro del presupuesto (${presupuesto_max - total:,} disponibles)"
    else:
        resultado += f"❌ Sobrepasa el presupuesto por ${total - presupuesto_max:,}"
    
    return resultado


@tool
def evaluar_balance_nutricional(productos_seleccionados: str) -> str:
    """Evalúa el balance nutricional de los productos seleccionados.
    
    Args:
        productos_seleccionados: Lista de nombres de productos separados por coma
    
    Returns:
        Análisis del balance entre categorías nutricionales
    """
    productos_lista = [p.strip().lower() for p in productos_seleccionados.split(',')]
    
    categorias_nutricionales = {
        'Proteínas': 0,
        'Frutas/Verduras': 0,
        'Lácteos': 0,
        'Cereales': 0,
        'Otros': 0
    }
    
    for nombre_prod in productos_lista:
        for p in productos:
            if nombre_prod in p['nombre'].lower():
                cat = p['categoria'].lower()
                if 'carne' in cat or 'pescado' in cat:
                    categorias_nutricionales['Proteínas'] += 1
                elif 'fruta' in cat or 'verdura' in cat:
                    categorias_nutricionales['Frutas/Verduras'] += 1
                elif 'lacteo' in cat or 'queso' in cat:
                    categorias_nutricionales['Lácteos'] += 1
                elif 'pan' in cat or 'cereal' in cat or 'desayuno' in cat:
                    categorias_nutricionales['Cereales'] += 1
                else:
                    categorias_nutricionales['Otros'] += 1
                break
    
    resultado = "🥗 BALANCE NUTRICIONAL:\n\n"
    for categoria, cantidad in categorias_nutricionales.items():
        if cantidad > 0:
            resultado += f"  • {categoria}: {cantidad} productos\n"
    
    resultado += "\nRecomendaciones:\n"
    if categorias_nutricionales['Frutas/Verduras'] < 3:
        resultado += "  ⚠️ Considera agregar más frutas y verduras\n"
    if categorias_nutricionales['Proteínas'] == 0:
        resultado += "  ⚠️ Falta fuente de proteína\n"
    if categorias_nutricionales['Lácteos'] == 0:
        resultado += "  ⚠️ Considera agregar lácteos\n"
    
    if not any('⚠️' in resultado for _ in range(1)):
        resultado += "  ✅ Balance nutricional adecuado"
    
    return resultado


# --- Herramientas de Escritura ---

@tool
def generar_carro_optimizado(tipo_dieta: str, presupuesto: float, personas: int) -> str:
    """Genera un carro de compras optimizado según parámetros.
    
    Args:
        tipo_dieta: Tipo de dieta ('vegetariana', 'diabetica', 'fitness', 'familiar')
        presupuesto: Presupuesto máximo en CLP
        personas: Número de personas
    
    Returns:
        Carro de compras generado con productos, precios y justificación
    """
    queries_dieta = {
        'vegetariana': 'frutas verduras lácteos huevos legumbres cereales',
        'diabetica': 'verduras carnes magras lácteos sin azúcar cereales integrales',
        'fitness': 'proteínas pollo pavo atún huevos avena frutas verduras',
        'familiar': 'frutas verduras carnes lácteos pan cereales snacks'
    }
    
    query = queries_dieta.get(tipo_dieta.lower(), queries_dieta['familiar'])
    
    num_productos = min(20, int(presupuesto / 1000))
    results = vectorstore.similarity_search(query, k=num_productos * 2)
    
    productos_seleccionados = []
    total = 0
    
    for doc in results:
        precio = doc.metadata['precio']
        if total + precio <= presupuesto:
            productos_seleccionados.append({
                'nombre': doc.metadata['nombre'],
                'precio': precio,
                'categoria': doc.metadata['categoria']
            })
            total += precio
            
            if len(productos_seleccionados) >= num_productos:
                break
    
    resultado = f"🛒 CARRO DE COMPRAS - Dieta {tipo_dieta.upper()}\n"
    resultado += f"👥 Para {personas} personas | 💰 Presupuesto: ${presupuesto:,}\n\n"
    resultado += "Productos seleccionados:\n\n"
    
    for i, p in enumerate(productos_seleccionados, 1):
        resultado += f"{i}. {p['nombre']}\n"
        resultado += f"   💵 ${p['precio']:,} | 📁 {p['categoria']}\n"
    
    resultado += f"\n💰 TOTAL: ${total:,} CLP\n"
    resultado += f"💵 Saldo restante: ${presupuesto - total:,} CLP\n"
    
    return resultado


@tool
def guardar_preferencias_usuario(nombre_usuario: str, preferencias: str) -> str:
    """Guarda las preferencias del usuario para futuras sesiones.
    
    Args:
        nombre_usuario: Identificador del usuario
        preferencias: Preferencias en formato texto
    
    Returns:
        Confirmación de guardado
    """
    archivo_preferencias = "data/preferencias_usuarios.json"
    
    try:
        if os.path.exists(archivo_preferencias):
            with open(archivo_preferencias, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        else:
            datos = {}
        
        datos[nombre_usuario] = {
            'preferencias': preferencias,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(archivo_preferencias, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        
        return f"✅ Preferencias guardadas para '{nombre_usuario}'"
    except Exception as e:
        return f"❌ Error al guardar preferencias: {str(e)}"


print("✅ Herramientas definidas (7 herramientas)")
print()

# ============================================================================
# CREACIÓN DEL AGENTE
# ============================================================================

# Lista de todas las herramientas
tools = [
    buscar_productos,
    obtener_estadisticas_categorias,
    validar_dieta,
    calcular_presupuesto,
    evaluar_balance_nutricional,
    generar_carro_optimizado,
    guardar_preferencias_usuario
]

# Prompt del sistema con planificación adaptativa
system_message = """Eres GROZY, un agente inteligente especializado en optimización de compras de supermercado.

TU OBJETIVO: Ayudar a usuarios a crear carros de compra optimizados según sus necesidades.

CAPACIDADES:
1. 🔍 Consulta: Puedes buscar productos y obtener estadísticas
2. 🧠 Razonamiento: Puedes validar dietas, calcular presupuestos y evaluar balance nutricional
3. ✍️ Escritura: Puedes generar carros optimizados y guardar preferencias

PLANIFICACIÓN ADAPTATIVA:
- Si el usuario pide un carro de compras, usa la herramienta generar_carro_optimizado directamente
- Si falta información, solicítala antes de generar el carro
- Si el presupuesto es insuficiente, sugiere alternativas más económicas
- Usa las herramientas disponibles para dar respuestas precisas

TONO: Amigable, profesional y proactivo. Usa emojis moderadamente.
"""

# Crear agente
agent_executor = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_message,
    debug=False
)

print("✅ Agente GROZY creado exitosamente")
print()

# ============================================================================
# INTERFAZ DE CHAT
# ============================================================================

def chat_interactivo():
    """Interfaz de chat interactivo con el agente."""
    print("="*60)
    print("🤖 AGENTE GROZY - Chat Interactivo")
    print("="*60)
    print("Comandos especiales:")
    print("  • 'salir' - Terminar conversación")
    print("  • 'ayuda' - Ver ejemplos de uso")
    print("="*60)
    print()
    
    conversation_messages = []
    
    while True:
        user_input = input("🧑 Tú: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ['salir', 'exit', 'quit']:
            print("\n👋 ¡Hasta luego! Gracias por usar GROZY.\n")
            break
        
        if user_input.lower() == 'ayuda':
            print("\n📖 EJEMPLOS DE USO:")
            print("  • ¿Qué productos tienes disponibles?")
            print("  • Dame estadísticas de productos")
            print("  • Genera un carro vegetariano para 3 personas con $25000")
            print("  • Busca productos lácteos bajos en grasa")
            print("  • Valida si [productos] son aptos para dieta diabética\n")
            continue
        
        try:
            # Agregar mensaje del usuario
            conversation_messages.append(HumanMessage(content=user_input))
            
            # Invocar agente
            print("\n🤖 GROZY está pensando...\n")
            respuesta = agent_executor.invoke({"messages": conversation_messages})
            
            # Actualizar historial con todos los mensajes
            conversation_messages = respuesta['messages']
            
            # Mostrar respuesta
            respuesta_texto = respuesta['messages'][-1].content
            print(f"🤖 GROZY:\n{respuesta_texto}\n")
            print("-"*60)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Conversación interrumpida. ¡Hasta luego!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            print("Intenta reformular tu pregunta.\n")


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    try:
        chat_interactivo()
    except KeyboardInterrupt:
        print("\n\n👋 Programa terminado.\n")
    except Exception as e:
        print(f"\n❌ Error fatal: {str(e)}\n")
