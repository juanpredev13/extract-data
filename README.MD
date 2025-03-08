# 🛠️ Extracción de Contenido desde HTML y JSON

Este proyecto permite extraer contenido de blogs y páginas HTML, clasificarlos y guardarlos en archivos JSON individuales basados en su `post_id`.

## 📂 Estructura del Proyecto

```
/proyecto
│── html/ (no repo)        # Carpeta con los archivos HTML/XML extraídos
│── output_json/ (no repo) # Carpeta donde se guardan los archivos JSON generados
│── filtered_final.json    # JSON con la lista de archivos a procesar
│── extract_content.py     # Script para extraer contenido
│── requirements.txt       # Archivo con las dependencias necesarias
│── README.md              # Documentación del proyecto
```

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/juanpredev13/extract-data.git
cd extract-data
```

### 2. Creación de un Entorno Virtual

Para evitar conflictos con otras dependencias, se recomienda utilizar un entorno virtual.

#### Crear un entorno virtual:

```bash
python -m venv env
```

#### Activar el entorno virtual:

**En Windows:**

```bash
env\Scripts\activate
```

**En Mac/Linux:**

```bash
source env/bin/activate
```

### 3. Instalación de Dependencias

```bash
pip install -r requirements.txt
```

Si no tienes un archivo `requirements.txt`, puedes crearlo ejecutando:

```bash
pip freeze > requirements.txt
```

## 📌 Uso

Para ejecutar el script y extraer contenido de los archivos HTML:

```bash
python extract_content.py
```

El script procesará todos los archivos listados en `filtered_final.json`, clasificando el contenido como **blog o página**, y guardará cada entrada en la carpeta `output_json/` con su respectivo `post_id`.

## 📝 ¿Qué hace el script?

1. **Carga la lista de archivos desde `filtered_final.json`**.
2. **Verifica si cada archivo es un blog o una página estática**.
3. **Extrae información relevante**, como:
   - Título
   - Autor (si es un blog)
   - Fecha de publicación (si es un blog)
   - Categorías (si es un blog)
   - Contenido principal
4. **Guarda los datos en archivos JSON individuales en `output_json/`** con el nombre basado en el `post_id`.

### 📂 Ejemplo de Salida

#### Blog (`output_json/165.json`)

```json
{
    "title": "Agricultura libre de agrotóxicos como motor del Turismo de Salud y Bienestar",
    "slug": "agricultura-libre-agrotoxicos",
    "type": "blog",
    "categories": "Interés General",
    "author": "crazul",
    "date": "31 enero, 2013",
    "content": "Anteayer el doctor Christian Rivera, coordinador de Costa Rica Azul..."
}
```

## 📌 Personalización

Si deseas extraer más detalles, puedes modificar el script `extract_content.py` en las siguientes secciones:

- **Imágenes destacadas**: Agregar extracción de `<meta property="og:image">`.
- **Enlaces dentro del contenido**: Buscar todas las etiquetas `<a>` dentro del contenido.
- **Etiquetas adicionales**: Extraer metadatos como etiquetas o palabras clave.

---

## 🛠️ Contribución

Si deseas mejorar el script:

1. **Haz un fork** del repositorio.
2. **Crea una nueva rama** para tu mejora:
   
   ```bash
   git checkout -b mejora-extraccion
   ```
   
3. **Sube tus cambios y haz un pull request**.

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. ¡Úsalo libremente y contribuye! 🚀

