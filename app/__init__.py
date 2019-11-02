from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager

application = Flask(__name__)
applicationlication.config.from_object(Config)

db = SQLAlchemy(application)
migrate = Migrate(application, db)

login = LoginManager(application)
login.login_view = 'login'


from application import routes, models

if not application.debug and not application.testing:
        # ...

        if application.config['LOG_TO_STDOUT']:
            # stream_handler = logging.StreamHandler()
            # stream_handler.setLevel(logging.INFO)
            # application.logger.addHandler(stream_handler)
            pass
        else:
            # if not os.path.exists('logs'):
            #     os.mkdir('logs')
            # file_handler = RotatingFileHandler('logs/microblog.log',
            #                                    maxBytes=10240, backupCount=10)
            # file_handler.setFormatter(logging.Formatter(
            #     '%(asctime)s %(levelname)s: %(message)s '
            #     '[in %(pathname)s:%(lineno)d]'))
            # file_handler.setLevel(logging.INFO)
            # application.logger.addHandler(file_handler)
            pass

        # application.logger.setLevel(logging.INFO)
        application.logger.info('Microblog startup')