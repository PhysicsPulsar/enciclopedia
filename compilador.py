"""
Generador de HTML para Enciclopedia FyQ (versión comentada y con feedback)
==========================================================================

Este script convierte archivos Markdown (.md) en páginas HTML usando una
plantilla base.

MEJORAS DE ESTA VERSIÓN:
- Mensajes de éxito y error en cada fase
- Comentarios explicativos para principiantes
- Manejo básico de errores
- Registro de progreso del build

Autor: Enciclopedia FyQ
"""

import re
from pathlib import Path
import traceback


# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

# Carpeta donde están los artículos en Markdown
ARTICLES_DIR = "articulos"

# Carpeta donde se generan los HTML finales
OUTPUT_DIR = "build"

# Plantilla HTML base
TEMPLATE_PATH = "templates/articulo.html"


# =========================================================
# UTILIDADES BÁSICAS DE ARCHIVOS
# =========================================================

def read_file(path):
    """Lee un archivo y devuelve su contenido"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"[ERROR] No se pudo leer el archivo: {path}")
        print(e)
        return None


def write_file(path, content):
    """Escribe contenido en un archivo, creando carpetas si es necesario"""
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"[OK] Archivo generado: {path}")

    except Exception as e:
        print(f"[ERROR] No se pudo escribir el archivo: {path}")
        print(e)


# =========================================================
# PARSEO INLINE (negrita, cursiva, enlaces)
# =========================================================

def parse_inline(text):
    """Convierte formato Markdown básico dentro de una línea"""

    try:
        # Negrita **texto**
        text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)

        # Cursiva *texto*
        text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)

        # Enlaces [texto](url)
        text = re.sub(r"\[(.*?)\]\((.*?)\)", r"<a href='\2'>\1</a>", text)

        return text

    except Exception as e:
        print("[ERROR] Fallo en parse_inline")
        print(e)
        return text


# =========================================================
# BLOQUES ESPECIALES (@image, @note, etc.)
# =========================================================

def parse_special_blocks(lines):
    """Procesa bloques especiales del Markdown"""

    html = []

    try:
        for line in lines:
            line = line.strip()

            # -----------------------------
            # IMÁGENES
            # @image ruta | pie
            # -----------------------------
            if line.startswith("@image"):
                try:
                    parts = line.replace("@image", "").strip().split("|")
                    src = parts[0].strip()
                    caption = parts[1].strip() if len(parts) > 1 else ""

                    html.append(f"""
<div class='image-container'>
    <img src='{src}' alt='imagen'>
    <p class='image-caption'>{caption}</p>
</div>
""")

                    print(f"[OK] Imagen procesada: {src}")

                except Exception:
                    print("[ERROR] Error procesando @image")

                continue

            # -----------------------------
            # NOTAS
            # @note texto
            # -----------------------------
            if line.startswith("@note"):
                content = line.replace("@note", "").strip()
                html.append(f"<div class='note-box'>{content}</div>")

                print("[OK] Nota procesada")
                continue

            # -----------------------------
            # SUBTÍTULOS
            # @subtitle texto
            # -----------------------------
            if line.startswith("@subtitle"):
                content = line.replace("@subtitle", "").strip()
                html.append(f"<p class='article-subtitle'>{content}</p>")

                print("[OK] Subtítulo procesado")
                continue

            # Si no es especial, lo ignoramos aquí
            html.append(line)

    except Exception as e:
        print("[ERROR] Fallo en parse_special_blocks")
        print(traceback.format_exc())

    return html


# =========================================================
# MARKDOWN A HTML BÁSICO
# =========================================================

def markdown_to_html(md):
    """Convierte Markdown simple a HTML"""

    try:
        lines = md.split("\n")
        html = []

        in_code = False
        code_buffer = []

        for line in lines:
            stripped = line.strip()

            # -----------------------------
            # BLOQUES DE CÓDIGO
            # -----------------------------
            if stripped.startswith("```"):
                in_code = not in_code

                if not in_code:
                    html.append("<pre><code>" + "\n".join(code_buffer) + "</code></pre>")
                    code_buffer = []
                    print("[OK] Bloque de código procesado")

                continue

            if in_code:
                code_buffer.append(line)
                continue

            # -----------------------------
            # TÍTULOS
            # -----------------------------
            if stripped.startswith("###"):
                html.append(f"<h3>{parse_inline(stripped[3:].strip())}</h3>")
            elif stripped.startswith("##"):
                html.append(f"<h2>{parse_inline(stripped[2:].strip())}</h2>")
            elif stripped.startswith("#"):
                html.append(f"<h1>{parse_inline(stripped[1:].strip())}</h1>")

            # -----------------------------
            # PÁRRAFOS
            # -----------------------------
            elif stripped != "":
                html.append(f"<p>{parse_inline(stripped)}</p>")

        print("[OK] Markdown convertido a HTML")
        return "\n".join(html)

    except Exception as e:
        print("[ERROR] Fallo en markdown_to_html")
        print(traceback.format_exc())
        return ""


# =========================================================
# GENERACIÓN DE ARTÍCULO
# =========================================================

def build_article(md_path):
    """Genera un HTML desde un archivo Markdown"""

    print(f"\n[INFO] Procesando: {md_path}")

    try:
        md = read_file(md_path)
        if md is None:
            print("[ERROR] Markdown vacío o no encontrado")
            return

        template = read_file(TEMPLATE_PATH)
        if template is None:
            print("[ERROR] Template no encontrado")
            return

        # Convertimos Markdown a HTML
        content_html = markdown_to_html(md)

        # Nombre del artículo
        title = Path(md_path).stem.replace("-", " ").title()

        # Insertamos en plantilla
        final_html = template.replace("{{CONTENT}}", content_html)
        final_html = final_html.replace("{{TITLE}}", title)

        # Guardar resultado
        output_path = Path(OUTPUT_DIR) / (Path(md_path).stem + ".html")
        write_file(output_path, final_html)

        print(f"[SUCCESS] Articulo generado correctamente: {title}")

    except Exception:
        print("[FATAL ERROR] Error construyendo artículo")
        print(traceback.format_exc())


# =========================================================
# GENERAR TODOS LOS ARTÍCULOS
# =========================================================

def build_all():
    """Procesa todos los .md de la carpeta articulos"""

    print("\n==============================")
    print(" INICIANDO GENERACION MASIVA ")
    print("==============================\n")

    try:
        files = list(Path(ARTICLES_DIR).glob("*.md"))

        if not files:
            print("[WARNING] No se encontraron archivos Markdown")
            return

        print(f"[INFO] Archivos encontrados: {len(files)}")

        for md_file in files:
            build_article(md_file)

        print("\n[OK] Proceso completado")

    except Exception:
        print("[FATAL ERROR] Error en build_all")
        print(traceback.format_exc())


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    build_all()
