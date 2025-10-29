"""
GROZY API - Backend Flask para el Chatbot Web
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import create_agent

# Cargar variables de entorno
load_dotenv()

# Crear aplicación Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS para peticiones desde el navegador

# ============================================================================
# CONFIGURACIÓN Y CARGA DE DATOS (Una sola vez al iniciar)
# ============================================================================

print("🔄 Inicializando GROZY Agent...")

# Credenciales
github_token = os.getenv('GITHUB_TOKEN')
openai_base_url = os.getenv('OPENAI_BASE_URL')

if not github_token:
    raise ValueError("Configura GITHUB_TOKEN en el archivo .env")

# Cargar productos
file_path = os.path.join("data", "productos_unimarc_muestra.json")
with open(file_path, "r", encoding="utf-8") as f:
    productos = json.load(f)

# Convertir a documentos
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

# Crear vector store
embeddings = OpenAIEmbeddings(
    api_key=github_token,
    base_url=openai_base_url,
    model="text-embedding-3-small"
)

vectorstore = FAISS.from_documents(docs, embeddings)

# Configurar LLM
llm = ChatOpenAI(
    api_key=github_token,
    base_url=openai_base_url,
    model="gpt-4o-mini",
    temperature=0.7
)

# ============================================================================
# DEFINICIÓN DE HERRAMIENTAS
# ============================================================================

@tool
def buscar_productos(query: str, k: int = 10) -> str:
    """Busca productos en la base de datos."""
    results = vectorstore.similarity_search(query, k=k)
    productos_encontrados = []
    
    for doc in results:
        productos_encontrados.append(
            f"- {doc.metadata['nombre']} | ${doc.metadata['precio']} | {doc.metadata['categoria']}"
        )
    
    return f"Productos encontrados ({len(productos_encontrados)}):\n" + "\n".join(productos_encontrados)


@tool
def obtener_estadisticas_categorias() -> str:
    """Obtiene estadísticas de productos por categoría."""
    categorias = {}
    precios_por_cat = {}
    
    for p in productos:
        cat = p['categoria']
        categorias[cat] = categorias.get(cat, 0) + 1
        if cat not in precios_por_cat:
            precios_por_cat[cat] = []
        precios_por_cat[cat].append(p['precio'])
    
    resultado = "📊 ESTADÍSTICAS:\n\n"
    resultado += f"Total productos: {len(productos)}\n"
    resultado += f"Categorías: {len(categorias)}\n\n"
    
    for cat, count in sorted(categorias.items(), key=lambda x: x[1], reverse=True)[:8]:
        precio_prom = sum(precios_por_cat[cat]) / len(precios_por_cat[cat])
        resultado += f"• {cat}: {count} productos (${precio_prom:,.0f})\n"
    
    return resultado


@tool
def generar_carro_optimizado(tipo_dieta: str, presupuesto: float, personas: int) -> str:
    """Genera un carro de compras optimizado."""
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
    
    resultado = f"🛒 CARRO - Dieta {tipo_dieta.upper()}\n"
    resultado += f"👥 {personas} personas | 💰 ${presupuesto:,}\n\n"
    
    for i, p in enumerate(productos_seleccionados, 1):
        resultado += f"{i}. {p['nombre']} - ${p['precio']:,}\n"
    
    resultado += f"\n💰 TOTAL: ${total:,}\n"
    resultado += f"💵 Saldo: ${presupuesto - total:,}\n"
    
    return resultado


# Crear agente
tools = [buscar_productos, obtener_estadisticas_categorias, generar_carro_optimizado]

system_message = """Eres GROZY, un asistente de compras de supermercado.

Ayudas a los usuarios a:
- Buscar productos
- Ver estadísticas
- Generar carros de compra optimizados

Cuando el usuario pida un carro, usa generar_carro_optimizado directamente.
Sé breve y directo. Usa emojis moderadamente."""

agent_executor = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_message,
    debug=False
)

print("✅ GROZY Agent listo")

# ============================================================================
# ALMACENAMIENTO DE SESIONES (En memoria - simple)
# ============================================================================

# Diccionario para almacenar conversaciones por sesión
sessions = {}

# ============================================================================
# ENDPOINTS DE LA API
# ============================================================================

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint para enviar mensajes al agente."""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Mensaje vacío'}), 400
        
        # Obtener o crear historial de sesión
        if session_id not in sessions:
            sessions[session_id] = []
        
        conversation_messages = sessions[session_id]
        
        # Agregar mensaje del usuario
        conversation_messages.append(HumanMessage(content=user_message))
        
        # Invocar agente
        respuesta = agent_executor.invoke({"messages": conversation_messages})
        
        # Actualizar historial
        sessions[session_id] = respuesta['messages']
        
        # Extraer respuesta del agente
        respuesta_texto = respuesta['messages'][-1].content
        
        return jsonify({
            'response': respuesta_texto,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset():
    """Endpoint para reiniciar una sesión."""
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        
        if session_id in sessions:
            del sessions[session_id]
        
        return jsonify({'message': 'Sesión reiniciada', 'session_id': session_id})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint para verificar el estado del servidor."""
    return jsonify({
        'status': 'ok',
        'agent': 'GROZY',
        'version': '1.0',
        'products': len(productos),
        'tools': len(tools)
    })


@app.route('/')
def index():
    """Página de inicio."""
    return '''
    <h1>GROZY API</h1>
    <p>API funcionando correctamente.</p>
    <p>Endpoints disponibles:</p>
    <ul>
        <li>POST /api/chat - Enviar mensaje</li>
        <li>POST /api/reset - Reiniciar sesión</li>
        <li>GET /api/health - Estado del servidor</li>
    </ul>
    '''


# ============================================================================
# EJECUTAR SERVIDOR
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Servidor GROZY API iniciado")
    print("="*60)
    print("📡 URL: http://localhost:5000")
    print("📖 Documentación: http://localhost:5000")
    print("\nPresiona Ctrl+C para detener el servidor\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
