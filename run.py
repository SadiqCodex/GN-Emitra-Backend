from app import create_app
from flask_cors import CORS

app = create_app()

# Enable CORS and specify allowed origin(s)
CORS(app, resources={r"/*": {"origins": "https://gn-emitra.netlify.app"}})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
