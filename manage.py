import os
import sys
import io
from app import create_app, db, redis_store
from app.models import Bus, User, Order
from flask_script import Manager, Shell

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def make_shell_context():
    return dict(app=app, db=db, Bus=Bus, User=User, Order=Order, redis=redis_store)


app = create_app('proConfig')

manager = Manager(app)
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
