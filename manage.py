import os
from app import create_app, db
from flask_script import Manager, Shell
from app.models import User, Role, Permission, Post, Follow, Comment
from flask_migrate import MigrateCommand, Migrate

import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

app = create_app(os.getenv('MYBLOG_CONFIG') or 'default')
manage = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Permission=Permission, Post=Post, Follow=Follow, Comment=Comment)
manage.add_command('shell', Shell(make_context=make_shell_context))
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manage.run()