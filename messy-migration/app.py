from flask import Flask
from routes.user_routes import user_bp
from db import close_db

app = Flask(__name__)
app.register_blueprint(user_bp)
app.teardown_appcontext(close_db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)