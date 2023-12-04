import os
from flask import Flask
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    load_dotenv()

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from flaskr.db import db
    db.connectDB()    
    
    from flaskr.utils.email_helper import EmailSender
    app.config['MAIL_SERVER'] = "smtp.googlemail.com"
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    EmailSender.get_instance().init_app(app)
    
    # error handler
    from flaskr.errors.bad_request import BadRequestError
    from flaskr.errors.not_found import NotFoundError
    from flaskr.errors.unauthenicated import UnauthenticatedError
    from flaskr.errorHandlers.my_handler import my_handler
    from flaskr.errorHandlers.default_http_handler import default_http_handler
    from flaskr.errorHandlers.default_handler import default_handler
    app.register_error_handler(BadRequestError, my_handler)
    app.register_error_handler(NotFoundError, my_handler)
    app.register_error_handler(UnauthenticatedError, my_handler)
    app.register_error_handler(HTTPException, default_http_handler)
    app.register_error_handler(Exception, default_handler)
    
    # api/v1/auth
    from flaskr.controllers.authController import authBP
    app.register_blueprint(authBP)
    
    # api/v1/workspace

    return app