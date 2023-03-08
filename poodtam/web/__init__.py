__version__ = "0.1.1"

from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import optparse
import pathlib
import os


from . import views, oauth, acl, redis_rq
from .. import models

app = Flask(__name__)


def create_app():
    app.config.from_object("poodtam.default_settings")
    app.config.from_envvar("POODTAM_SETTINGS", silent=True)

    SECRET_KEY = os.urandom(32)
    app.config.update(
        SECRET_KEY=SECRET_KEY,
        SESSION_COOKIE_SECURE=False,
        WTF_CSRF_ENABLED=False,
        WTF_CSRF_METHODS=[],
        WTF_CSRF_CHECK_DEFAULT=False,
    )

    csrf = CSRFProtect()
    csrf.init_app(app)
    login_manager = LoginManager()  # Login manager for flask-login # New
    login_manager.init_app(app)

    POODTAM_CACHE_DIR = app.config.get("POODTAM_CACHE_DIR")
    p = pathlib.Path(POODTAM_CACHE_DIR)
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)

    models.init_db(app)
    views.register_blueprint(app)
    oauth.init_oauth(app)
    oauth.init_bcrypt(app)
    acl.init_acl(app)
    redis_rq.init_rq(app)

    return app


def get_program_options(default_host="127.0.0.1", default_port="8080"):
    """
    Takes a flask.Flask instance and runs it. Parses
    command-line flags to configure the app.
    """

    parser = optparse.OptionParser()
    parser.add_option(
        "-H",
        "--host",
        help="Hostname of the Flask app " + "[default %s]" % default_host,
        default=default_host,
    )
    parser.add_option(
        "-P",
        "--port",
        help="Port for the Flask app " + "[default %s]" % default_port,
        default=default_port,
    )

    parser.add_option(
        "-c", "--config", dest="config", help=optparse.SUPPRESS_HELP, default=None
    )
    parser.add_option(
        "-d", "--debug", action="store_true", dest="debug", help=optparse.SUPPRESS_HELP
    )
    parser.add_option(
        "-p",
        "--profile",
        action="store_true",
        dest="profile",
        help=optparse.SUPPRESS_HELP,
    )

    options, _ = parser.parse_args()

    return options
