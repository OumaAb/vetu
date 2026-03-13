# catalog_service.py
# Microservice 2: Clothes Catalog (View all clothes)
# Runs on port 5002
#
# Run with: python catalog_service.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_connection


app = Flask(__name__)
CORS(app)


@app.route("/clothes", methods=["GET"])
def get_all_clothes():
    """Get all clothes. Optional filter by category or size."""
    category = request.args.get("category")   
    size = request.args.get("size")           
    available_only = request.args.get("available", "false").lower() == "true"

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Build query dynamically based on filters
        query = "SELECT * FROM clothes WHERE 1=1"
        params = []

        if category:
            query += " AND category = %s"
            params.append(category)
        if size:
            query += " AND size = %s"
            params.append(size)
        if available_only:
            query += " AND available = TRUE"

        query += " ORDER BY created_at DESC"
        cursor.execute(query, params)
        clothes = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify(clothes), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/clothes/<int:cloth_id>", methods=["GET"])
def get_cloth(cloth_id):
    """Get a single cloth by ID."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clothes WHERE id = %s", (cloth_id,))
        cloth = cursor.fetchone()
        cursor.close()
        conn.close()

        if not cloth:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(cloth), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/categories", methods=["GET"])
def get_categories():
    """Get all unique categories."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM clothes ORDER BY category")
        categories = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("👗 Catalog Service running on http://localhost:5002")
    app.run(port=5002, host="0.0.0.0", debug=True)
