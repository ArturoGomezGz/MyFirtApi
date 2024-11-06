from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/get-user/<user_id>")
def home(user_id):
    data = {
        "userId": user_id,
        "userName": "Arturo Gomez"
    }

    return jsonify(data), 200


if __name__ == "__main__":
    app.run(debug=True)