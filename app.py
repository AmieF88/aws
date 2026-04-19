from flask import Flask, request, jsonify
from database_config import get_connection

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "Flask API is running"}), 200


@app.route("/add_person", methods=["POST"])
def add_person():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        address = data.get("address")
        age = data.get("age")

        if not first_name or not last_name or not address or age is None:
            return jsonify({
                "error": "first_name, last_name, address, and age are required"
            }), 400

        conn = get_connection()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO persons (first_name, last_name, address, age)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """
        cursor.execute(insert_query, (first_name, last_name, address, age))
        person_id = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Person added successfully",
            "id": person_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_persons", methods=["GET"])
def get_persons():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        select_query = """
            SELECT id, first_name, last_name, address, age
            FROM persons
            ORDER BY id;
        """
        cursor.execute(select_query)
        rows = cursor.fetchall()

        persons = []
        for row in rows:
            persons.append({
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "address": row[3],
                "age": row[4]
            })

        cursor.close()
        conn.close()

        return jsonify(persons), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)