# run.py

from app import create_app
from flask_cors import CORS

app = create_app()
CORS(app)  # Enable CORS globally

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
