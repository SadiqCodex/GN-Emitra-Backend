import os
from app import create_app

# Create the Flask app (with CORS already configured inside create_app)
app = create_app()

if __name__ == "__main__":
    # Get port from environment variable, default to 5000
    port = int(os.getenv("PORT", 5000))

    # Get debug mode from environment variable, default to True
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"

    # Run the app
    app.run(host="0.0.0.0", port=port, debug=debug)
