from .upload import extracao_bp

def register_blueprint(app):
    app.register_blueprint(extracao_bp)