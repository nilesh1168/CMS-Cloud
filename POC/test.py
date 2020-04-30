from flask import url_for
from flask_login import current_user
from POC.app_tests.test_base import BaseTestCase
from POC.models import Admin
from POC import db

class AdminViewsTests(BaseTestCase):
    
    def test_admin_can_login(self):
        admin = Admin(username='admin',email='admin@abc.com',mobile=1234567890)
        admin.set_password('pass')
        db.session.add(admin)
        db.session.commit()
        with self.client:
            response = self.client.post(url_for('login'),data={'username': 'admin', 'password': 'pass'})
            self.assert_redirects(response, url_for('home'))
            self.assertTrue(current_user.username == 'admin')
            self.assertFalse(current_user.is_anonymous)        

    def test_users_can_logout(self):
        admin = Admin(username='admin',email='admin@abc.com',mobile=1234567890)
        admin.set_password('pass')
        db.session.add(admin)
        db.session.commit()
        with self.client:
            self.client.post(url_for('login'),data={'username': 'admin', 'password': 'pass'})
            self.client.get(url_for("logout"))
            self.assertTrue(current_user.is_anonymous)        

    def test_invalid_password_is_rejected(self):
        admin = Admin(username='admin',email='admin@abc.com',mobile=1234567890)
        admin.set_password('pass')
        db.session.add(admin)
        db.session.commit()
        with self.client:
            self.client.post("login", data={"username": "admin", "password": "****"}) 
            self.assertTrue(current_user.is_anonymous)
      
    def test_service_worker(self):
        self.assert200(self.client.get("/service-worker.js"))
            
    def test_json_city(self):
        response = self.client.get("/getCity?city=Satara")
        self.assertEqual(response.json, dict(students=[]))  
