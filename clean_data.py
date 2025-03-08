import json

# Ruta del archivo original y el de salida
input_file = "structure.json"  # Archivo limpio actual
output_file = "filtered_structure.json"  # Archivo final sin URLs no deseadas

# Palabras clave a eliminar en las URLs
keywords_to_remove = [
    "/author/",
    "blog-masonry-2-columns",
    "blog-masonry-3",
    "blog-masonry",
    "blog-grid",
    "blog-grid-2-columns",
    "blog-grid-3-column",
    "blog-grid-full-width",
    "blog-grid-left-sidebar",
    "blog-grid-right-sidebar",
    "blog-classic-fullwidth",
    "blog-classic-left-sidebar",  
    "blog-classic-right-sidebar",
    "wp-json/oembed/1.0/embed?url=",
    "wp-login.php?redirect_to=",
    "/wp-includes/",
    "/wp-admin/",
    "/wp-content/"
]

# Cargar el JSON
with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Filtrar los registros eliminando los que contengan las palabras clave
filtered_data = []
removed_count = 0

for entry in data:
    if any(keyword in entry["url"] for keyword in keywords_to_remove):
        print(f"❌ Eliminado: {entry['url']}", flush=True)  # `flush=True` mantiene los prints visibles
        removed_count += 1
    else:
        filtered_data.append(entry)

# Guardar el JSON limpio
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(filtered_data, file, indent=4, ensure_ascii=False)

# Mensaje final
print("\n✅ Proceso completado.")
print(f"❌ Total de enlaces eliminados: {removed_count}")
print(f"📂 Archivo guardado en: {output_file}")
