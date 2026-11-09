
import os
import json
import mimetypes
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "phishing_model.pkl")
HTML_PATH = os.path.join(BASE_DIR, "templates", "index.html")
STATIC_DIR = os.path.join(BASE_DIR, "static")

model = joblib.load(MODEL_PATH)


def application(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "/")

    # Homepage
    if method == "GET" and path == "/":
        if not os.path.isfile(HTML_PATH):
            return respond(start_response, "500 Internal Server Error",
                           b"Homepage file not found on server.")

        with open(HTML_PATH, "rb") as file:
            content = file.read()

        return respond(start_response, "200 OK", content, "text/html")

    # CSS and JavaScript
    if method == "GET" and path.startswith("/static/"):
        filename = os.path.basename(path)

        if filename not in ("style.css", "script.js"):
            return respond(start_response, "404 Not Found", b"File not found.")

        filepath = os.path.join(STATIC_DIR, filename)

        if not os.path.isfile(filepath):
            return respond(start_response, "404 Not Found", b"Static file not found.")

        with open(filepath, "rb") as file:
            content = file.read()

        content_type = mimetypes.guess_type(filepath)[0] or "application/octet-stream"
        return respond(start_response, "200 OK", content, content_type)

    # Email prediction
    if method == "POST" and path == "/predict":
        try:
            length = int(environ.get("CONTENT_LENGTH") or 0)

            if length <= 0 or length > 100000:
                return json_response(start_response, {"error": "Invalid email text size."}, "400 Bad Request")

            data = json.loads(environ["wsgi.input"].read(length))
            email = data.get("email", "").strip()

            if not isinstance(email, str) or not email:
                return json_response(start_response, {"error": "Please enter email content."}, "400 Bad Request")

            prediction = int(model.predict([email])[0])
            probabilities = model.predict_proba([email])[0]
            phishing_probability = probabilities[list(model.classes_).index(1)]

            result = "Potential Phishing Email" if prediction == 1 else "Legitimate Email"

            return json_response(start_response, {
                "prediction": result,
                "phishing_probability": round(float(phishing_probability) * 100, 2)
            })

        except Exception:
            return json_response(start_response, {"error": "Unable to analyse the email."}, "500 Internal Server Error")

    return respond(start_response, "404 Not Found", b"Page not found.")


def respond(start_response, status, content, content_type="text/plain"):
    start_response(status, [
        ("Content-Type", content_type),
        ("Content-Length", str(len(content))),
        ("Cache-Control", "no-store")
    ])
    return [content]


def json_response(start_response, data, status="200 OK"):
    content = json.dumps(data).encode("utf-8")
    return respond(start_response, status, content, "application/json")
