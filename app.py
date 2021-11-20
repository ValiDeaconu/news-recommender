import os
from flask import Flask, send_from_directory, session
from flask_session import Session
from model import db
from rest import Blueprints

import client

class FlaskWrapper(Flask):
    def init(self):
        for bp in Blueprints:
            self.register_blueprint(bp[1], url_prefix=bp[0])

        # Register template endpoints
        self.register_blueprint(client.blueprint)

        self.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.config['UPLOAD_FOLDER'] = 'invoices'
        self.config['ASSETS_FOLDER'] = os.path.join('templates', 'assets')
        self.config['IMAGES_FOLDER'] = os.path.join('templates', 'images')
        self.config['SESSION_TYPE'] = 'filesystem'
        self.config['SECRET_KEY'] = 'secret'
        self.secret_key = 'secret'

        sess = Session()
        sess.init_app(self)

    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
            with self.app_context():
                db.init_app(self)
                db.create_all()

        super(FlaskWrapper, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


app = FlaskWrapper(__name__)

# Serve static data
@app.route('/assets/<path:path>')
def serve_asset(path: str):
    return send_from_directory(directory=app.config['ASSETS_FOLDER'], path=path)
    
@app.route('/images/<path:path>')
def serve_image(path: str):
    return send_from_directory(directory=app.config['IMAGES_FOLDER'], path=path)

# Entrypoint
if __name__ == '__main__':
    app.init()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))