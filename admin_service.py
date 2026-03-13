# admin_service.py
# Microservice 4: Admin Panel (Add, Update, Delete clothes)
# Runs on port 5004
#
# Run with: python admin_service.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests # It lets Python call another service
from db import get_connection


app = Flask(__name__)
CORS(app)

AUTH_SERVICE = "http://auth-service:5001"


def get_admin_user(token):
    """Verify token AND check that user is an admin."""
    try:
        response = requests.get(
            f"{AUTH_SERVICE}/verify",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            user = response.json()["user"]
            if user.get("role") == "admin":
                return user
        return None
    except:
        return None


def get_token():
    return request.headers.get("Authorization", "").replace("Bearer ", "")


# ---- ADD A NEW CLOTHING ITEM ----
@app.route("/admin/clothes", methods=["POST"])
def add_cloth():
    """Admin: Add a new clothing item."""
    admin = get_admin_user(get_token())
    if not admin:
        return jsonify({"error": "Admin access required"}), 403

    data = request.json
    name = data.get("name")
    description = data.get("description", "")
    category = data.get("category")
    size = data.get("size")
    price_per_day = data.get("price_per_day")
    image_url = data.get("image_url", "")

    if not all([name, category, size, price_per_day]):
        return jsonify({"error": "name, category, size, price_per_day are required"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO clothes (name, description, category, size, price_per_day, image_url)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (name, description, category, size, price_per_day, image_url)
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"message": "Clothing item added!", "id": new_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---- UPDATE A CLOTHING ITEM ----
@app.route("/admin/clothes/<int:cloth_id>", methods=["PUT"])
def update_cloth(cloth_id):
    """Admin: Update an existing clothing item."""
    admin = get_admin_user(get_token())
    if not admin:
        return jsonify({"error": "Admin access required"}), 403

    data = request.json

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Build update query dynamically (only update provided fields)
        fields = []
        values = []

        for field in ["name", "description", "category", "size", "price_per_day", "image_url", "available"]:
            if field in data:
                fields.append(f"{field} = %s")
                values.append(data[field])

        if not fields:
            return jsonify({"error": "No fields to update"}), 400

        values.append(cloth_id)
        query = f"UPDATE clothes SET {', '.join(fields)} WHERE id = %s"
        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Item not found"}), 404

        cursor.close()
        conn.close()
        return jsonify({"message": "Item updated successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---- DELETE A CLOTHING ITEM ----
@app.route("/admin/clothes/<int:cloth_id>", methods=["DELETE"])
def delete_cloth(cloth_id):
    """Admin: Delete a clothing item."""
    admin = get_admin_user(get_token())
    if not admin:
        return jsonify({"error": "Admin access required"}), 403

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clothes WHERE id = %s", (cloth_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Item not found"}), 404

        cursor.close()
        conn.close()
        return jsonify({"message": "Item deleted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---- GET ALL RENTALS (admin view) ----
@app.route("/admin/rentals", methods=["GET"])
def all_rentals():
    """Admin: View all rentals."""
    admin = get_admin_user(get_token())
    if not admin:
        return jsonify({"error": "Admin access required"}), 403

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.*, u.name AS user_name, u.email, c.name AS cloth_name
            FROM rentals r
            JOIN users u ON r.user_id = u.id 
            JOIN clothes c ON r.cloth_id = c.id
            ORDER BY r.created_at DESC
        """) #This is a JOIN — it pulls data from 3 tables at once instead of making 3 separate queries
        rentals = cursor.fetchall()
        for r in rentals:
            r["start_date"] = str(r["start_date"])
            r["end_date"] = str(r["end_date"])
            r["created_at"] = str(r["created_at"]) #MySQL date objects can't be converted to JSON automatically — str() fixes that.
        cursor.close()
        conn.close()
        return jsonify(rentals), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---- GET ALL CLOTHES (admin view with full details) ----
@app.route("/admin/clothes", methods=["GET"])
def admin_get_clothes():
    """Admin: Get all clothes including unavailable ones."""
    admin = get_admin_user(get_token())
    if not admin:
        return jsonify({"error": "Admin access required"}), 403

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clothes ORDER BY created_at DESC")
        clothes = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(clothes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("🔧 Admin Service running on http://localhost:5004")
    app.run(port=5004, host="0.0.0.0", debug=True)
