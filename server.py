
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
import json
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(BASE_DIR)

model = joblib.load("phishing_model.pkl")


class SecurityHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        if urlparse(self.path).path != "/predict":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            if length > 100000:
                self.send_json({"error": "Email text is too large."}, 413)
                return

            data = json.loads(self.rfile.read(length))
            email = data.get("email", "").strip()

            if not email:
                self.send_json({"error": "Please enter email content."}, 400)
                return

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

            self.send_json({
                "prediction": result,
                "phishing_probability": round(
                    float(phishing_probability) * 100, 2
                )
            })

        except (ValueError, TypeError, json.JSONDecodeError):
            self.send_json({"error": "Invalid request."}, 400)
        except Exception:
            self.send_json({"error": "Unable to analyse the email."}, 500)

    def send_json(self, data, status=200):
        response = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), SecurityHandler)
    print("Server running at http://127.0.0.1:8000")
    server.serve_forever()
