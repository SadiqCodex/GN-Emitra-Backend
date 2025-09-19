# app/routes/review.py

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from flask_cors import cross_origin
from app.extensions.db import get_db_connection
import os

review_bp = Blueprint('review', __name__)

# POST review
@review_bp.route('/api/review', methods=['POST'])
@cross_origin(origins=["https://gn-emitra.netlify.app", "http://localhost:5502"])
def submit_review():
    try:
        data = request.form
        image = request.files.get('image')

        image_url = None
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = f'/uploads/{filename}'

        # Save to Postgres
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO reviews (name, city, rating, comment, image_url)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (
            data.get("name"),
            data.get("city"),
            data.get("rating"),
            data.get("comment"),
            image_url
        ))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success", "message": "Review saved.", "id": new_id}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# GET review by ID
@review_bp.route('/api/review/<int:review_id>', methods=['GET'])
@cross_origin(origins=["https://gn-emitra.netlify.app", "http://localhost:5502"])
def get_review(review_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, name, city, rating, comment, image_url, created_at
            FROM reviews
            WHERE id = %s
        """, (review_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            review = {
                "id": row[0],
                "name": row[1],
                "city": row[2],
                "rating": row[3],
                "comment": row[4],
                "image_url": row[5],
                "created_at": row[6].isoformat()
            }
            return jsonify(review), 200
        else:
            return jsonify({"status": "error", "message": "Review not found"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# DELETE review by ID
@review_bp.route('/api/review/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM reviews WHERE id = %s RETURNING id", (review_id,))
        deleted = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if deleted:
            return jsonify({"status": "success", "message": f"Review {review_id} deleted."}), 200
        else:
            return jsonify({"status": "error", "message": "Review not found"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# GET all reviews
@review_bp.route('/api/reviews', methods=['GET'])
def get_all_reviews():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, name, city, rating, comment, image_url, created_at
            FROM reviews
            ORDER BY created_at DESC
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        reviews = [{
            "id": row[0],
            "name": row[1],
            "city": row[2],
            "rating": row[3],
            "comment": row[4],
            "image_url": row[5],
            "created_at": row[6].isoformat()
        } for row in rows]

        return jsonify(reviews), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# DELETE all reviews + reset ID sequence
@review_bp.route('/api/reviews', methods=['DELETE'])
def delete_all_reviews():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Delete all rows
        cur.execute("DELETE FROM reviews")
        # Reset SERIAL id sequence
        cur.execute("ALTER SEQUENCE reviews_id_seq RESTART WITH 1")
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success", "message": "All reviews deleted and ID reset."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
