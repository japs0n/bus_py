import os
import sys
import io
from app import create_app
from flask_script import Manager, Shell

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def make_shell_context():
    return dict(app=app)


app = create_app(os.getenv('FLSAK_CONFIG') or 'default')

manager = Manager(app)
manager.add_command('shell', Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
