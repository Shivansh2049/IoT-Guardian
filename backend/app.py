from flask import Flask
from flask_cors import CORS
from api.scan import scan_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # ✅ Register the scan API under /api
    app.register_blueprint(scan_bp, url_prefix="/api")

    @app.route("/")
    def home():
        return {"message": "IoT Guardian backend running"}

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

