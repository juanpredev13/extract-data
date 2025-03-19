import json
import re
import os

# Ruta del archivo original y el de salida
input_file = "filtered_structure.json"
output_file = "filtered_pages.json"

# Si el archivo es XML, ignorarlo
if input_file.lower().endswith(".xml"):
    print("❌ Archivo XML detectado. No se procesará.")
    exit()

# Palabras clave y patrones a eliminar
keywords_to_remove = {
    "/author/", "/category/", "/tag/",
    "/blog/",  # Filtra cualquier URL de blogs
    "blog-masonry-2-columns", "blog-masonry-3", "blog-masonry",
    "blog-grid", "blog-grid-2-columns", "blog-grid-3-column",
    "blog-grid-full-width", "blog-grid-left-sidebar", "blog-grid-right-sidebar",
    "blog-classic-fullwidth", "blog-classic-left-sidebar", "blog-classic-right-sidebar",
    "home-blog-large-image", "header-layout-01", "header-layout-02", "header-layout-03",
    "header-layout-04", "header-layout-05", "header-layout-06", "header-layout-07",
    "header-menu-customize", "header-menu-fullwidth", "header-menu-sticky",
    "header-menu-transparent", "header-menu-float", "heading-shortcode",
    "portfolio-category", "wp-json/oembed/1.0/embed?url=",
    "wp-login.php?redirect_to=", "/wp-includes/", "/wp-admin/", "/wp-content/",
    "whatsapp-image", "whatsapp-video"
}

regex_patterns_to_remove = [
    re.compile(r"blog/page/\d+/"),  # Excluye URLs como blog/page/60/
    re.compile(r"blog/(201[0-9]|202[0-5])/\d{2}/"),  # Excluye blog/YYYY/MM/
    re.compile(r"blog/\?p=\d+"),  # Excluye URLs como blog/?p=1173
    re.compile(r"/(19[0-9]{2}|20[0-9]{2})/\d{2}/\d{2}/"),  # Excluye /YYYY/MM/DD/
]

# Función para filtrar URLs y asegurarse de que sean páginas
def is_valid_url(entry):
    url = entry.get("url", "")

    # Excluir si contiene alguna palabra clave no deseada
    if any(keyword in url for keyword in keywords_to_remove):
        return False

    # Excluir si coincide con algún patrón de blog
    if any(pattern.search(url) for pattern in regex_patterns_to_remove):
        return False

    # Asegurar que sea una página válida
    return "/page/" not in url and "/blog/" not in url

# Cargar, filtrar y guardar JSON
if os.path.exists(input_file):
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    filtered_data = [entry for entry in data if is_valid_url(entry)]
    removed_count = len(data) - len(filtered_data)
    
    # Contar páginas únicas
    unique_pages = {entry["url"] for entry in filtered_data}
    total_pages = len(unique_pages)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(filtered_data, file, indent=4, ensure_ascii=False)

    # Mensaje final
    print(f"\n✅ Proceso completado.")
    print(f"❌ Total eliminados: {removed_count}")
    print(f"📄 Total de páginas únicas después del filtrado: {total_pages}")
    print(f"📂 Archivo guardado en: {output_file}")
else:
    print("❌ Archivo de entrada no encontrado.")
