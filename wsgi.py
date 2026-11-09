
import json
import os
import joblib
from urllib.parse import parse_qs

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "phishing_model.pkl"))

def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")

    if method == "GET" and path == "/":
        file_path = os.path.join(BASE_DIR, "templates", "index.html")
        content_type = "text/html; charset=utf-8"

    elif method == "GET" and path in (
        "/static/style.css",
        "/static/script.js"
    ):
        filename = os.path.basename(path)
        file_path = os.path.join(BASE_DIR, "static", filename)

        content_type = (
            "text/css; charset=utf-8"
            if filename.endswith(".css")
            else "application/javascript; charset=utf-8"
        )

    elif method == "POST" and path == "/predict":
        try:
            length = int(environ.get("CONTENT_LENGTH") or 0)

            if length > 100000:
                raise ValueError("Email text is too large.")

            body = environ["wsgi.input"].read(length)
            data = json.loads(body.decode("utf-8"))

            email = data.get("email", "").strip()

            if not email:
                raise ValueError("Please enter email content.")

            prediction = int(model.predict([email])[0])
            probabilities = model.predict_proba([email])[0]

            phishing_probability = probabilities[
                list(model.classes_).index(1)
            ]

            result = (
                "Potential Phishing Email"
                if prediction == 1
                else "Legitimate Email"
            )

            response = json.dumps({
                "prediction": result,
                "phishing_probability": round(
                    float(phishing_probability) * 100, 2
                )
            }).encode("utf-8")

            start_response("200 OK", [
                ("Content-Type", "application/json"),
                ("Content-Length", str(len(response))),
                ("Cache-Control", "no-store")
            ])
            return [response]

        except ValueError as error:
            message = str(error)
            status = "413 Payload Too Large" if message == "Email text is too large." else "400 Bad Request"
        except (TypeError, json.JSONDecodeError, UnicodeDecodeError):
            message = "Invalid request."
            status = "400 Bad Request"
        except Exception:
            message = "Unable to analyse the email."
            status = "500 Internal Server Error"

        response = json.dumps({"error": message}).encode("utf-8")
        start_response(status, [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(response)))
        ])
        return [response]

    else:
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"Page not found"]

    try:
        with open(file_path, "rb") as file:
            content = file.read()

        start_response("200 OK", [
            ("Content-Type", content_type),
            ("Content-Length", str(len(content)))
        ])
        return [content]

    except FileNotFoundError:
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"File not found"]
