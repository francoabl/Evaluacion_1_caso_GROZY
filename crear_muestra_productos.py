import json
import random

# Leer el archivo original
with open("data/productos_unimarc.json", "r", encoding="utf-8") as f:
    productos_completos = json.load(f)

print(f"Total de productos originales: {len(productos_completos)}")

# Agrupar productos por categoría
productos_por_categoria = {}
for producto in productos_completos:
    categoria = producto['categoria']
    if categoria not in productos_por_categoria:
        productos_por_categoria[categoria] = []
    productos_por_categoria[categoria].append(producto)

print(f"\nCategorías encontradas: {len(productos_por_categoria)}")
for categoria, productos in productos_por_categoria.items():
    print(f"  - {categoria}: {len(productos)} productos")

# Seleccionar una muestra diversa
productos_seleccionados = []
productos_por_categoria_meta = 25  # 25 productos por categoría

# Priorizar categorías vegetarianas y diversas
categorias_prioritarias = ['frutas', 'verduras', 'lacteos', 'panaderia', 'bebidas', 'snacks', 'cereales', 'conservas']

# Primero agregar productos de categorías prioritarias
for categoria in categorias_prioritarias:
    if categoria in productos_por_categoria:
        productos_categoria = productos_por_categoria[categoria]
        # Filtrar productos con precio > 0
        productos_con_precio = [p for p in productos_categoria if p['precio'] > 0]
        if len(productos_con_precio) > 0:
            muestra = random.sample(productos_con_precio, min(productos_por_categoria_meta, len(productos_con_precio)))
            productos_seleccionados.extend(muestra)
            print(f"Agregados {len(muestra)} productos de {categoria}")

# Luego agregar productos de otras categorías hasta completar ~500 productos
target_total = 500
categorias_restantes = [cat for cat in productos_por_categoria.keys() if cat not in categorias_prioritarias]

productos_por_categoria_resto = max(5, (target_total - len(productos_seleccionados)) // len(categorias_restantes))

for categoria in categorias_restantes:
    if len(productos_seleccionados) >= target_total:
        break
    
    productos_categoria = productos_por_categoria[categoria]
    productos_con_precio = [p for p in productos_categoria if p['precio'] > 0]
    
    if len(productos_con_precio) > 0:
        cantidad_a_tomar = min(productos_por_categoria_resto, len(productos_con_precio), target_total - len(productos_seleccionados))
        muestra = random.sample(productos_con_precio, cantidad_a_tomar)
        productos_seleccionados.extend(muestra)
        print(f"Agregados {len(muestra)} productos de {categoria}")

print(f"\nTotal de productos seleccionados: {len(productos_seleccionados)}")

# Mezclar aleatoriamente
random.shuffle(productos_seleccionados)

# Guardar la muestra
with open("data/productos_unimarc_muestra.json", "w", encoding="utf-8") as f:
    json.dump(productos_seleccionados, f, ensure_ascii=False, indent=2)

print(f"\n✅ Archivo creado: data/productos_unimarc_muestra.json")
print(f"✅ Productos incluidos: {len(productos_seleccionados)}")

# Mostrar resumen por categoría de la muestra
categorias_muestra = {}
for producto in productos_seleccionados:
    categoria = producto['categoria']
    categorias_muestra[categoria] = categorias_muestra.get(categoria, 0) + 1

print(f"\n📊 Distribución por categoría en la muestra:")
for categoria, cantidad in sorted(categorias_muestra.items()):
    print(f"  - {categoria}: {cantidad} productos")