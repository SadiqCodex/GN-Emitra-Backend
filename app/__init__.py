# app/__init__.py

from flask import Flask, send_from_directory
from dotenv import load_dotenv
import os

# Load environment variables (for local dev)
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuration from env vars or defaults
    app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_FOLDER", "uploads")
    app.config['REVIEW_FILE'] = os.getenv("REVIEW_FILE", "reviews.json")

    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Root route
    @app.route('/')
    def home():
        return "✅ Flask API is running!"

    # Serve uploaded images
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Register blueprints
    from app.routes.review import review_bp
    app.register_blueprint(review_bp)

    return app
