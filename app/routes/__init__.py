def create_app():
    app = Flask(__name__)
    ...

    from app.routes.user_routes import reset_users
    reset_users()

    app.register_blueprint(user_bp, url_prefix='/api/users')
    ...
    return app
