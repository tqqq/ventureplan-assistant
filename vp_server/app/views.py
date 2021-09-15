# coding=utf-8
from flask.views import MethodView


class VPView(MethodView):

    def post(self):

        # put data to queue

        return 'hello'
