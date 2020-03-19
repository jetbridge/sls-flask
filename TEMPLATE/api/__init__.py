from flask_smorest import Api

api = Api()


def init_views():
    from . import monitor, auth

    apis = (monitor, auth)

    # get exported "blp" blueprint objects
    for blp in (a.blp for a in apis):
        api.register_blueprint(blp)
