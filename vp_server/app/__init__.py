# coding=utf-8

from flask import Blueprint

from .views import VPView

bp_vp = Blueprint(name='wow_assistant', import_name=__name__, url_prefix='/wow_assistant')

bp_vp.add_url_rule('/vp', view_func=VPView.as_view(name='venture_plan'), methods=['POST'])
