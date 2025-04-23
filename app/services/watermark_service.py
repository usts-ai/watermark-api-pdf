import os
import tempfile
import subprocess
import io

def apply_watermark_to_pdf(pdf_file, watermark_content, is_image=False, pattern='grid', options=None):
    """
    Applique un filigrane à un fichier PDF.
    
    Args:
        pdf_file: Le fichier PDF à traiter (FileStorage ou BytesIO)
        watermark_content: Le texte ou le chemin vers l'image du filigrane
        is_image: Indique si le filigrane est une image
        pattern: Le motif à utiliser ('grid' ou 'insert')
        options: Dictionnaire contenant les options supplémentaires
        
    Returns:
        tuple: (chemin_sortie, est_temporaire) où est_temporaire indique si le fichier doit être supprimé après utilisation
    """
    if options is None:
        options = {}
    
    # Créer un fichier temporaire pour l'entrée
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as input_temp:
        # Gérer différents types d'objets de fichier
        if hasattr(pdf_file, 'save'):
            # Pour les objets FileStorage (request.files)
            pdf_file.save(input_temp.name)
        elif isinstance(pdf_file, io.BytesIO) or hasattr(pdf_file, 'read'):
            # Pour les objets BytesIO ou tout objet avec une méthode read()
            pdf_file.seek(0)  # Remettre le curseur au début
            input_temp.write(pdf_file.read())
        else:
            raise TypeError("Le type de fichier PDF n'est pas pris en charge")
            
        input_path = input_temp.name
    
    # Créer un fichier temporaire pour la sortie
    output_path = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False).name
    
    try:
        # Construire la commande watermark
        command = ['watermark']
        
        # Ajouter le type de motif et les chemins d'entrée/sortie
        command.append(pattern)
        command.append(input_path)
        command.append(watermark_content)
        command.extend(['-s', output_path])
        
        # Options communes
        if 'opacity' in options:
            command.extend(['-o', options['opacity']])
        
        if 'angle' in options:
            command.extend(['-a', options['angle']])
        
        if 'text_color' in options:
            command.extend(['-tc', options['text_color']])
        
        if 'text_font' in options:
            command.extend(['-tf', options['text_font']])
        
        if 'text_size' in options:
            command.extend(['-ts', options['text_size']])
        
        if options.get('unselectable') == 'true':
            command.append('--unselectable')
        
        if 'image_scale' in options:
            command.extend(['-is', options['image_scale']])
        
        if options.get('save_as_image') == 'true':
            command.append('--save-as-image')
        
        if 'dpi' in options:
            command.extend(['--dpi', options['dpi']])
        
        # Options spécifiques au motif
        if pattern == 'grid':
            if 'horizontal_boxes' in options:
                command.extend(['-h', options['horizontal_boxes']])
            
            if 'vertical_boxes' in options:
                command.extend(['-v', options['vertical_boxes']])
            
            if options.get('margin') == 'true':
                command.append('-m')
        
        else:  # pattern == 'insert'
            if 'x' in options:
                command.extend(['-x', options['x']])
            
            if 'y' in options:
                command.extend(['-y', options['y']])
            
            if 'horizontal_alignment' in options:
                command.extend(['-ha', options['horizontal_alignment']])
        
        # Exécuter la commande
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Erreur lors de l'application du filigrane: {result.stderr}")
        
        return output_path, True
    
    except Exception as e:
        # Nettoyer les fichiers en cas d'erreur
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        raise e
    
    finally:
        # Nettoyer le fichier d'entrée
        if os.path.exists(input_path):
            os.remove(input_path)
