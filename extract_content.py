import os
import json
import warnings
from urllib.parse import urlparse
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

# Filtrar advertencias de XML interpretado como HTML
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Directorios
BASE_PATH = "html"  # Ajusta la ruta donde están los archivos HTML/XML
INPUT_JSON = "filtered_final.json"  # JSON con lista de archivos
OUTPUT_DIR = "output_json"  # Carpeta para los archivos extraídos

# Crear carpeta de salida si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cargar el JSON con la lista de archivos
print("📂 Cargando JSON de estructura...")
try:
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        pages = json.load(f)
        print(f"✅ JSON cargado correctamente. Total de posts: {len(pages)}")
except Exception as e:
    print(f"❌ Error cargando el JSON: {e}")
    exit()

# Función para extraer contenido de blogs y páginas
def extract_content(file_path, url):
    try:
        # Determinar si el archivo es XML o HTML
        is_xml = file_path.endswith(".xml")

        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "xml" if is_xml else "lxml")

            # Extraer título
            title = soup.title.string.strip() if soup.title else "Sin título"

            # Extraer slug desde la URL
            parsed_url = urlparse(url)
            slug = parsed_url.path.strip("/").split("/")[-1] if parsed_url.path else "sin-slug"

            # Identificar si es un blog o una página estándar
            is_blog = bool(soup.find("div", class_="entry"))  # Buscar estructura de blog

            if is_blog:
                # Extraer contenido del blog
                content_div = soup.find("div", class_="entry")
                content_text = content_div.get_text(strip=True, separator="\n") if content_div else "Sin contenido"

                # Extraer la categoría
                category = soup.find("span", class_="categories")
                category_text = category.get_text(strip=True) if category else "Sin categoría"

                # Extraer el autor
                author = soup.find("span", class_="author vcard")
                author_text = author.get_text(strip=True) if author else "Sin autor"

                # Extraer la fecha de publicación
                date = soup.find("abbr", class_="date time published")
                date_text = date.get_text(strip=True) if date else "Sin fecha"

                extracted_data = {
                    "title": title,
                    "slug": slug,
                    "type": "blog",
                    "categories": category_text,
                    "author": author_text,
                    "date": date_text,
                    "content": content_text
                }
            else:
                # Extraer contenido de una página estática
                main_content = soup.find("main") or soup.find("div", class_="entry-content")
                content_text = main_content.get_text(strip=True, separator="\n") if main_content else "Sin contenido"

                extracted_data = {
                    "title": title,
                    "slug": slug,
                    "type": "page",
                    "content": content_text
                }

            return extracted_data

    except Exception as e:
        print(f"⚠️ Error extrayendo contenido de {file_path}: {e}")
        return {
            "title": "Error",
            "slug": "error-slug",
            "type": "unknown",
            "content": "No se pudo extraer el contenido"
        }

# Procesar TODOS los posts
print(f"🔄 Procesando TODOS los archivos...")

processed_count = 0
total_posts = len(pages)

for index, page in enumerate(pages, start=1):
    filename = page["filename"]
    file_path = os.path.join(BASE_PATH, filename)
    url = page["url"]  # Obtener la URL del JSON
    post_id = page["post_id"]  # Obtener el número de post

    if os.path.exists(file_path):  # Verificar si el archivo existe
        print(f"📖 ({index}/{total_posts}) Extrayendo contenido de: {filename} ({url})")
        extracted_data = extract_content(file_path, url)

        # Guardar en un JSON individual con el post_id como nombre de archivo
        output_filename = f"{post_id}.json"
        output_file = os.path.join(OUTPUT_DIR, output_filename)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(extracted_data, f, indent=4, ensure_ascii=False)

        print(f"✅ Guardado: {output_file}")
        processed_count += 1
    else:
        print(f"❌ Archivo no encontrado: {file_path}")

print(f"\n🎉 Proceso completado. Se extrajeron {processed_count}/{total_posts} archivos.")
