# flask_testing/test_base.py
from flask_testing import TestCase

from POC.config import TestConfig
from POC import app, db



class BaseTestCase(TestCase):
    """A base test case for flask-tracking."""
    render_templates = False
    def create_app(self):
        app.config.from_object(TestConfig)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()