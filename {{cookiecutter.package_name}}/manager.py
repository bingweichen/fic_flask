import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import db, app
from config import config

# import for migration (not used)
# from app.user import model
# from app.post import model

# app = create_app(os.getenv('FLASK_CONFIG') or 'default')

app.config.from_object(config[os.getenv('FLASK_CONFIG') or 'default'])
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# with app.app_context():
#     if db.engine.url.drivername == 'sqlite':
#         migrate.init_app(app, db, render_as_batch=True)
#     else:
#         migrate.init_app(app, db)

if __name__ == "__main__":
    manager.run()
