import os
from app import create_app, db
from app.models import User, Role, Email
from flask_migrate import Migrate

app = create_app('default')
migrate = Migrate(app,db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Email=Email)

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestResult(verbosity=2).run(tests)