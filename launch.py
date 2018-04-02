from .app import create_app, db
from .app.models import User, Role
from flask_migrate import Migrate, MigrateCommand

app =create_app(os.getenv('FLASK_CONFIG') or 'default')
migrete = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

if __name__ == '__main__':
    app.run()
