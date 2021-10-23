import os
from flask import Flask

from server.controllers.user import user_bp
from server.controllers.error_handler import error_handler_bp
from server.controllers.index import index_bp

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.register_blueprint(error_handler_bp)
    app.register_blueprint(index_bp)
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))