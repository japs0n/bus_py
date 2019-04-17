# -*- coding: utf-8 -*-

from app import create_app
import datetime

application = app = create_app('proConfig')


@app.context_processor
def template_extras():
    return {'enumerate': enumerate, 'datetime': datetime}
