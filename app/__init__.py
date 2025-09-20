from flask import Flask, send_from_directory
from dotenv import load_dotenv
import os
from app.extensions.db import init_db  
from flask_cors import CORS

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_FOLDER", "uploads")

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Enable CORS here, before registering blueprints
    CORS(app, origins=[
        "https://gn-emitra.netlify.app",
        "http://localhost:5502",
        "http://127.0.0.1:5502"
    ], supports_credentials=True)

    init_db()

    from app.routes.review import review_bp
    app.register_blueprint(review_bp)

    @app.route('/')
    def home():
        return "✅ Flask API is running with Postgres!"

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app