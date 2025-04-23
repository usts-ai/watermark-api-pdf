import os
import tempfile
from flask import Blueprint, request, jsonify, send_file
from app.services.watermark_service import apply_watermark_to_pdf

watermark_bp = Blueprint('watermark', __name__)

@watermark_bp.route('/watermark', methods=['POST'])
def apply_watermark():
    """
    Endpoint pour appliquer un filigrane à un PDF.
    
    Paramètres attendus dans la requête:
    - file: Le fichier PDF à traiter (multipart/form-data)
    - text: Le texte à utiliser comme filigrane (form-data)
    - pattern: Le motif à utiliser (grid ou insert) (optionnel, défaut: grid)
    """
    # Vérifier si un fichier a été envoyé
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier n'a été fourni"}), 400
    
    pdf_file = request.files['file']
    
    # Vérifier si le fichier est un PDF
    if not pdf_file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Le fichier doit être au format PDF"}), 400
    
    # Vérifier si le texte ou l'image du filigrane a été fourni
    if 'text' not in request.form and 'image' not in request.files:
        return jsonify({"error": "Le texte ou l'image du filigrane n'a pas été fourni"}), 400
    
    # Déterminer si nous utilisons du texte ou une image comme filigrane
    is_image = False
    watermark_file_path = None
    
    if 'text' in request.form:
        watermark_content = request.form['text']
    else:
        watermark_file = request.files['image']
        # Créer un fichier temporaire pour l'image du filigrane
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(watermark_file.filename)[1]) as wm_temp:
            watermark_file.save(wm_temp.name)
            watermark_content = wm_temp.name
            watermark_file_path = wm_temp.name
        is_image = True
    
    pattern = request.form.get('pattern', 'grid')
    
    if pattern not in ['grid', 'insert']:
        return jsonify({"error": "Le motif doit être 'grid' ou 'insert'"}), 400
    
    # Extraire toutes les options du formulaire
    options = {key: value for key, value in request.form.items() 
               if key not in ['file', 'text', 'pattern']}
    
    try:
        # Appliquer le filigrane
        output_path, is_temp = apply_watermark_to_pdf(
            pdf_file=pdf_file,
            watermark_content=watermark_content,
            is_image=is_image,
            pattern=pattern,
            options=options
        )
        
        # Renvoyer le fichier PDF avec le filigrane
        return send_file(
            output_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"watermarked_{pdf_file.filename}"
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        # Nettoyer les fichiers temporaires
        if is_image and watermark_file_path and os.path.exists(watermark_file_path):
            os.remove(watermark_file_path)
        # Le fichier de sortie sera supprimé après l'envoi
