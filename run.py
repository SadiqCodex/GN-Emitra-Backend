from app import create_app
from flask_cors import CORS
import os

app = create_app()

CORS(app, origins=[
    "http://localhost:5502", 
    "http://127.0.0.1:5502", 
    "https://gn-emitra.netlify.app"
], supports_credentials=True)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
