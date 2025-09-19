from flask import Flask, send_from_directory
from dotenv import load_dotenv
import os
from app.extensions.db import init_db   # Database init import

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_FOLDER", "uploads")

    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize database tables
    init_db()

    # Root route
    @app.route('/')
    def home():
        return "✅ Flask API is running with Postgres!"

    # Serve uploaded images
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Register blueprints
    from app.routes.review import review_bp
    app.register_blueprint(review_bp)

    return app
