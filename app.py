from flask import Flask, render_template, url_for, request
import os
from translation import TECH_TRANSLATIONS

app = Flask(__name__)

ITEMS_PER_PAGE = 1

PROJECTS = [
    {
        "id": "UNGA80",
        "title": {
            "en": "Uses SQL to classify the subjects treated in UNGA80",
            "es": "Usa SQL para clasificar los temas tratados en la UNGA80"
        },
        "short": {
            "en": "Classifies subjects and indexes them by region",
            "es": "Clasifica los temas y los indexa por región"
        },
        "description": {
            "en": "Information summarized and divided by topic, country, and speaker",
            "es": "Información resumida y dividida por tema, país y orador"
        },
        "tech": ["Python", "Flask", "SQLAlchemy", "Celery", "Postgres", "transformers", "Whisper", "pandas"],
        "repo": "https://github.com/yourusername/inventory-audit",
        "screenshots": [
            "screenshots/UNGA.jpg",
            "screenshots/cotton.png",
        ]
    },
    {
        "id": "miga",
        "title": {
            "en": "System for rating raw materials and purchased goods, calculating tax, unit costs, recipes, customers, and finished products.",
            "es": "Sistema de calificación de materias primas, artículos compradps, cálculo de impuesto, costos por unidad, recetas, clientes y productos terminados"
        },
        "short": {
            "en": "Classify purchased products, enter raw materials, use XML validated by the Ministry of Finance in Costa Rica",
            "es": "Clasifica productos comprados, introduce materias primas, usa XML avalados por Hacienda en Costa Rica"
        },
        "description": {
            "en": "Creates SQL tables that will be key for big projects",
            "es": "crea tablas en SQL como llave de pendientes de proyectos"
        },
        "tech": ["Python", "Flask", "SQLAlchemy", "transformers", "Whisper", "Torch"],
        "repo": "https://github.com/yourusername/inventory-audit",
        "screenshots": [
            "screenshots/factura.png",
            "screenshots/ventaitem.png",
            "screenshots/producto.png",
            "screenshots/receta.jpg",
        ]
    },
    {
        "id": "App Audios",
        "title": {
            "en": "Create an SQL table with voice messages summarized by important topics and with a degree of importance to create pending tasks",
            "es": "crea tabla de SQL con mensajes de voz resumidos por temas importantes y con grados para crear pendientes"
        },
        "short": {
            "en": "Uses IA to summerize and transcribe audios",
            "es": "Utiliza IA para resumir y transcribir audios"
        },
        "description": {
            "en": "Information summarized and divided by topic, country, and speaker",
            "es": "Information on raw materials, recipes, customers, and orders"
        },
        "tech": ["Python", "Flask", "SQLAlchemy", "Celery", "pandas"],
        "repo": "https://github.com/yourusername/inventory-audit",
        "screenshots": [
            "screenshots/Transcript.png",
            "screenshots/tablet.png",
        ]
    },

]

@app.route("/")
def index():
    lang = request.args.get("lang", "en")
    page = int(request.args.get("page", 1))
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    paginated_projects = []
    for p in PROJECTS[start:end]:
        p2 = {
            "id": p["id"],
            "title": p["title"].get(lang, p["title"]["en"]),
            "short": p["short"].get(lang, p["short"]["en"]),
            "description": p["description"].get(lang, p["description"]["en"]),
            "repo": p["repo"]
        }

        # Translate tech stack
        p2["tech"] = [TECH_TRANSLATIONS.get(t, {}).get(lang, t) for t in p.get("tech", [])]

        # Screenshot URLs with fallback
        p2["screenshot_urls"] = [
            url_for("static", filename=img.replace("\\", "/"))
            if os.path.exists(os.path.join(app.static_folder, img.replace("\\", "/")))
            else url_for("static", filename="screenshots/placeholder.png")
            for img in p.get("screenshots", [])
        ]

        paginated_projects.append(p2)

    total_pages = (len(PROJECTS) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    return render_template("index.html", projects=paginated_projects, page=page, total_pages=total_pages, lang=lang)

@app.route("/workin")
def workin():
    lang = request.args.get("lang", "en")
    message = {
        "en": {
            "title": "Work in Progress",
            "body": "Thanks for your interest! I'm currently updating this section to reflect the latest work. Please check back soon."
        },
        "es": {
            "title": "Trabajo en Progreso",
            "body": "¡Gracias por tu interés! Actualmente estoy actualizando esta sección para reflejar el trabajo más reciente. Vuelve pronto."
        }
    }
    return render_template("workin.html", lang=lang, message=message[lang])

if __name__ == "__main__":
    app.run(debug=True)