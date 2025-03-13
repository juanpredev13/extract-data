import os
import json
import requests
from requests.auth import HTTPBasicAuth


# Configuración de WordPress desde variables de entorno
WP_URL = os.getenv("WP_URL", "http://costaricaazul.local")  # Reemplázalo si es necesario
API_URL = f"{WP_URL}/wp-json/wp/v2"
USERNAME = "juan"  # Usuario con permisos para crear posts
APP_PASSWORD = "B57X wMGU IttA 01ai Cz6E b6lU"  # Application Password de WordPress

if not APP_PASSWORD:
    raise ValueError("❌ ERROR: No se encontró la contraseña de la aplicación. Configúrala en el archivo .env")

# Directorio con los archivos JSON de los posts/páginas
OUTPUT_DIR = "output_json5"

# Autenticación con Application Passwords
session = requests.Session()
session.auth = HTTPBasicAuth(USERNAME, APP_PASSWORD)

# Función para obtener la lista de categorías desde WordPress
def get_categories():
    url = f"{API_URL}/categories"
    response = session.get(url)
    if response.status_code == 200:
        return {cat["name"].lower(): cat["id"] for cat in response.json()}
    print(f"⚠️ No se pudieron obtener categorías: {response.status_code} - {response.text}")
    return {}

# Función para obtener la lista de etiquetas desde WordPress
def get_tags():
    url = f"{API_URL}/tags"
    response = session.get(url)
    if response.status_code == 200:
        return {tag["name"].lower(): tag["id"] for tag in response.json()}
    print(f"⚠️ No se pudieron obtener etiquetas: {response.status_code} - {response.text}")
    return {}

# Función para crear una nueva etiqueta en WordPress
def create_tag(tag_name):
    url = f"{API_URL}/tags"
    payload = {"name": tag_name}
    response = session.post(url, json=payload)
    if response.status_code == 201:
        return response.json().get("id")
    print(f"⚠️ No se pudo crear la etiqueta: {tag_name} - {response.text}")
    return None

# Obtener categorías y etiquetas actuales en WordPress
categories_dict = get_categories()
tags_dict = get_tags()

# Función para verificar si un post o página ya existe en WordPress
def check_existing_content(title, content_type):
    url = f"{API_URL}/{content_type}?search={title}"
    response = session.get(url)
    if response.status_code == 200:
        items = response.json()
        for item in items:
            if item["title"]["rendered"].strip().lower() == title.strip().lower():
                print(f"🔍 {content_type.capitalize()} ya existe: {item['link']}")
                return True
    return False

# Función para crear un post o página en WordPress
def create_wp_content(post_data):
    content_type = "posts" if post_data["type"] == "blog" else "pages"
    
    if check_existing_content(post_data["title"], content_type):
        return f"⚠️ {content_type.capitalize()} ya existente, pero se procesará de todos modos."
    
    url = f"{API_URL}/{content_type}"
    
    payload = {
        "title": post_data.get("title", "Sin título"),
        "content": post_data.get("content", "Sin contenido"),
        "status": "publish",  # Puedes usar "draft" si no quieres publicarlo directamente
    }

    # Si es un post, agregar categorías y autor
    if post_data["type"] == "blog":
        category_names = post_data.get("categories", [])
        if isinstance(category_names, str):
            category_names = [category_names.lower()]
        category_ids = [categories_dict.get(cat, 1) for cat in category_names if cat in categories_dict] or [1]
        payload["categories"] = category_ids
        payload["author"] = 1  # ID del autor en WordPress (ajustar según necesidad)
    
    # Asociar etiquetas al post
    tag_names = post_data.get("tags", [])
    if isinstance(tag_names, str):
        tag_names = [tag_names.lower()]
    tag_ids = []
    for tag in tag_names:
        if tag in tags_dict:
            tag_ids.append(tags_dict[tag])
        else:
            new_tag_id = create_tag(tag)
            if new_tag_id:
                tags_dict[tag] = new_tag_id
                tag_ids.append(new_tag_id)
    
    if tag_ids:
        payload["tags"] = tag_ids
    
    try:
        response = session.post(url, json=payload)
        response.raise_for_status()
        response_json = response.json()
        return f"✅ Creado con éxito: {response_json['link']}"
    except requests.exceptions.HTTPError as http_err:
        return f"❌ Error HTTP: {http_err} - {response.text}"
    except requests.exceptions.RequestException as req_err:
        return f"❌ Error de conexión: {req_err}"
    except json.JSONDecodeError:
        return f"❌ Error al procesar la respuesta de WordPress: {response.text}"

# Procesar todos los archivos JSON en output_json/
for filename in sorted(os.listdir(OUTPUT_DIR)):
    if filename.endswith(".json"):
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, "r", encoding="utf-8") as file:
            post_data = json.load(file)
        
        print(f"📤 Creando {post_data['type']} - {post_data['title']} ...")
        response_message = create_wp_content(post_data)
        print(response_message)