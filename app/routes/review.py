# app/routes/review.py

from flask import Blueprint, request, jsonify, current_app
import os
import json
from werkzeug.utils import secure_filename
from flask_cors import cross_origin

review_bp = Blueprint('review', __name__)

@review_bp.route('/api/review', methods=['POST'])
@cross_origin(origins=["https://gn-emitra.netlify.app", "http://localhost:5502"])
def submit_review():
    try:
        data = request.form
        image = request.files.get('image')

        # Save image if provided
        image_url = None
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = f'/uploads/{filename}'  # Public URL

        review = {
            "name": data.get("name"),
            "city": data.get("city"),
            "email": data.get("email"),
            "rating": data.get("rating"),
            "comment": data.get("comment"),
            "image_url": image_url
        }

        # Save to review file
        review_file = current_app.config['REVIEW_FILE']
        if not os.path.exists(review_file):
            with open(review_file, 'w') as f:
                json.dump([], f)

        with open(review_file, 'r+') as f:
            reviews = json.load(f)
            reviews.append(review)
            f.seek(0)
            json.dump(reviews, f, indent=4)

        return jsonify({"status": "success", "message": "Review saved."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@review_bp.route('/api/review', methods=['GET'])
@cross_origin(origins=["https://gn-emitra.netlify.app", "http://localhost:5502"])
def get_reviews():
    try:
        review_file = current_app.config['REVIEW_FILE']
        if not os.path.exists(review_file):
            return jsonify([]), 200

        with open(review_file, 'r') as f:
            reviews = json.load(f)

        return jsonify(reviews), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
