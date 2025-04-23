from flask import Flask

def create_app():
    """Initialise et configure l'application Flask."""
    app = Flask(__name__)
    
    # Importer et enregistrer les routes
    from app.routes.main import main_bp
    from app.routes.watermark import watermark_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(watermark_bp)
    
    return app
