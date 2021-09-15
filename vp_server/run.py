# coding=utf-8
import os
import sys
from flask import Flask

from vp_server.app import bp_vp


def create_app(root_path=None):
    if root_path is None:
        root_path = os.getcwd()
    sys.path.append(root_path)
    _app = Flask(__name__)

    # with _app.app_context():
    #     # init queue
    #     # load config
    #     # start engine
    #     pass

    _app.register_blueprint(bp_vp)

    return _app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=7002)
