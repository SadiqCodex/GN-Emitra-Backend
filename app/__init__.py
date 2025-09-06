from flask import Flask, send_from_directory
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_FOLDER", "uploads")
    app.config['REVIEW_FILE'] = os.getenv("REVIEW_FILE", "reviews.json")

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # ✅ Add a simple route for the root "/"
    @app.route('/')
    def home():
        return "✅ Flask API is running!"

    # Register blueprints
    from app.routes.review import review_bp
    app.register_blueprint(review_bp)

    # Serve uploaded images
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app
