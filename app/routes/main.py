from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def api_documentation():
    """Endpoint pour afficher la documentation de l'API."""
    docs = {
        "name": "API de Filigrane PDF",
        "description": "Cette API permet d'appliquer un filigrane (watermark) à un document PDF et de récupérer le document modifié.",
        "version": "1.0.0",
        "endpoints": [
            {
                "path": "/",
                "method": "GET",
                "description": "Affiche cette documentation"
            },
            {
                "path": "/watermark",
                "method": "POST",
                "description": "Applique un filigrane à un PDF",
                "parameters": {
                    "file": "Le fichier PDF à traiter (multipart/form-data)",
                    "text": "Le texte à utiliser comme filigrane (obligatoire si 'image' n'est pas fourni)",
                    "image": "L'image à utiliser comme filigrane (obligatoire si 'text' n'est pas fourni)",
                    "pattern": "Le motif à utiliser: 'grid' ou 'insert'. Défaut: 'grid'"
                },
                "options_communes": {
                    "opacity": "Opacité du filigrane entre 0 et 1",
                    "angle": "Angle d'inclinaison en degrés",
                    "text_color": "Couleur du texte au format hexadécimal, ex: #000000",
                    "text_font": "Police du texte",
                    "text_size": "Taille de la police",
                    "unselectable": "Rendre le texte non sélectionnable (true/false)",
                    "image_scale": "Facteur d'échelle pour l'image",
                    "save_as_image": "Convertir chaque page PDF en image (true/false)",
                    "dpi": "DPI à utiliser lors de la sauvegarde du PDF en image"
                },
                "options_grid": {
                    "horizontal_boxes": "Nombre de répétitions du filigrane horizontalement",
                    "vertical_boxes": "Nombre de répétitions du filigrane verticalement",
                    "margin": "Laisser une marge autour de la page (true/false)"
                },
                "options_insert": {
                    "x": "Position horizontale du filigrane (entre 0 et 1)",
                    "y": "Position verticale du filigrane (entre 0 et 1)",
                    "horizontal_alignment": "Alignement horizontal ('left', 'right', 'center')"
                }
            }
        ]
    }
    return jsonify(docs), 200
