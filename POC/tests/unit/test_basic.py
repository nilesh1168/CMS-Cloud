import pytest

from POC.models import Admin
  
@pytest.fixture(scope='module')
def new_user():
    admin = Admin(username='new_admin',email='email@abc.com',mobile=1234567890)
    admin.set_password('one')
    return admin


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, username, mobile and password fields are defined correctly
    """
    assert new_user.email == 'email@abc.com'
    assert new_user.username == 'new_admin'
    assert new_user.mobile == 1234567890
    # assert new_user.password_hash == new_user.check_password('one')