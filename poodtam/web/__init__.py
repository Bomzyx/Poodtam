__version__ = "0.1.1"

from flask import Flask
import optparse


import pathlib


from . import views, models

app = Flask(__name__)


def create_app():
    app.config.from_object("poodtam.default_settings")
    app.config.from_envvar("POODTAM_SETTINGS", silent=True)

    POODTAM_CACHE_DIR = app.config.get("POODTAM_CACHE_DIR")
    p = pathlib.Path(POODTAM_CACHE_DIR)
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)

    views.register_blueprint(app)

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

    if options.profile:
        from werkzeug.contrib.profiler import ProfilerMiddleware

        app.config["PROFILE"] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
        options.debug = True

    return options
