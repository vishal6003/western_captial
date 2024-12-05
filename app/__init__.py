from flask import Flask
from flask_cors import CORS
from .models import db
from .routes import bp

def create_app():
    app = Flask(__name__)
    CORS(app, resources={
        r"/*": {
            "origins": [
                "http://localhost:4200", 
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    app.config.from_object('app.config.Config')
    db.init_app(app)
    app.register_blueprint(bp)
    
    return app
