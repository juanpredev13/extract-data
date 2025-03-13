import os
import json
import warnings
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from multiprocessing import Pool, cpu_count

# Filtrar advertencias de XML interpretado como HTML
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Directorios
BASE_PATH = "html"  # Ajusta la ruta donde están los archivos HTML/XML
INPUT_JSON = "filtered_final.json"  # JSON con lista de archivos
OUTPUT_DIR = "output_json5"  # Carpeta para los archivos extraídos

# Crear carpeta de salida si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Expresiones regulares para excluir ciertos formatos de URLs
regex_patterns_to_remove = [
    re.compile(r"/blog/\d{4}/\d{2}/"),  # Excluir URLs del tipo /blog/2014/10/
    re.compile(r"/category/"),  # Excluir URLs con /category/
    re.compile(r"/tag/")  # Excluir URLs con /tag/
]

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
        # Evitar extraer desde archivos XML o URLs no deseadas
        if file_path.endswith(".xml") or any(pattern.search(url) for pattern in regex_patterns_to_remove):
            print(f"⚠️ Archivo o URL ignorado: {file_path} ({url})")
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "lxml")

            title = soup.title.string.strip() if soup.title else "Sin título"
            parsed_url = urlparse(url)
            slug = parsed_url.path.strip("/").split("/")[-1] if parsed_url.path else "sin-slug"

            # Identificar si es un blog basándose en la URL y la estructura del contenido
            is_blog = ("/blog/" in parsed_url.path) or (soup.find("div", class_="entry") or soup.find("article", class_="post"))
            
            # Identificar si es una página de etiquetas y evitar procesarla
            if soup.find("div", class_="title-bar") and soup.find("div", class_="title-bar").find("span", string="etiqueta"):
                print(f"⚠️ Página de etiquetas detectada y omitida: {file_path}")
                return None

            # Extraer tags de "entry-meta-tag-wrap"
            tags_section = soup.find("div", class_="entry-meta-tag-wrap")
            tags = [tag.get_text(strip=True) for tag in tags_section.find_all("a")] if tags_section else []

            # Eliminar contenido no deseado antes de extraer el texto
            for tag in soup.find_all(class_=["post-related-wrap", "entry-comments", "entry-meta-date"]):
                tag.decompose()

            if is_blog:
                content_div = soup.find("div", class_="entry") or soup.find("article", class_="post")
                content_text = content_div.get_text(strip=True, separator="\n") if content_div else ""
            else:
                main_content = soup.find("main") or soup.find("div", class_="entry-content")
                content_text = main_content.get_text(strip=True, separator="\n") if main_content else ""

            if not content_text.strip():
                print(f"⚠️ Entrada sin contenido ignorada: {file_path}")
                return None

            extracted_data = {
                "title": title,
                "slug": slug,
                "type": "blog" if is_blog else "page",
                "content": content_text,
                "tags": tags  # Agregar tags extraídos
            }

            return extracted_data

    except Exception as e:
        print(f"⚠️ Error extrayendo contenido de {file_path}: {e}")
        return None

# Función para procesar cada página
def process_page(page):
    filename = page["filename"]
    file_path = os.path.join(BASE_PATH, filename)
    url = page["url"]
    post_id = page["post_id"]

    if os.path.exists(file_path):
        extracted_data = extract_content(file_path, url)
        
        if extracted_data:
            output_filename = f"{post_id}.json"
            output_file = os.path.join(OUTPUT_DIR, output_filename)

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(extracted_data, f, indent=4, ensure_ascii=False)

            print(f"✅ Guardado: {output_file}")
            return 1
        else:
            print(f"⚠️ Archivo ignorado por falta de contenido o por ser una página de etiquetas: {file_path}")
            return 0
    else:
        print(f"❌ Archivo no encontrado: {file_path}")
        return 0

# Procesar todos los posts en paralelo
if __name__ == "__main__":
    print(f"🔄 Procesando archivos en paralelo usando {cpu_count()} núcleos...")
    with Pool(cpu_count()) as pool:
        processed_count = sum(pool.map(process_page, pages))

    print(f"\n🎉 Proceso completado. Se extrajeron {processed_count}/{len(pages)} archivos.")
