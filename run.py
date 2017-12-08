import os

from klein import Klein
from twisted.internet import _sslverify, reactor
from twisted.web.static import File

# import jsonpickle
from backend.api.doctor_house.consulting_api import add_doctor_house_consulting_routes
from backend.api.doctor_house.consulting_reply_api import add_doctor_house_consulting_reply_routes
from backend.api.random import add_random_routes
from backend.api.stocks import add_stocks_routes
from backend.api.user_wait import add_user_wait_routes
from backend.api.users import add_users_routes
from backend.database import close_data_db
from backend.websocket import web_socket_run

_sslverify.platformTrust = lambda: None

# jsonpickle.set_encoder_options('demjson', compactly=False)
# jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)

app = Klein()

add_random_routes(app)
add_stocks_routes(app)
add_users_routes(app)
add_user_wait_routes(app)

add_doctor_house_consulting_routes(app)
add_doctor_house_consulting_reply_routes(app)


@app.route('/static/', branch=True)
def static(_):
    return File('./dist/static')


@app.route("/")
def index(_):
    return File('./dist/index.html')


@app.route("/index.html")
def index(_):
    return File('./dist/index.html')


class ShutDown:
    stop = False


class ShuttingDown(Exception):
    pass


def serve():
    def shutdown():
        close_data_db()
        ShutDown.stop = True

    reactor.addSystemEventTrigger('before', 'shutdown', shutdown)

    port = int(os.environ.get('PORT', 5000))

    # web_socket_run('0.0.0.0', 9000)
    app.run("0.0.0.0", port)


if __name__ == '__main__':
    serve()
