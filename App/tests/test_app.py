import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Admin, Alumni, Company, Listing
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    add_admin,
    add_alumni,
    add_company,
    add_listing,
    subscribe_action,
    add_categories,
    apply_listing,
    get_all_applicants,
    get_alumni,
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    # def test_new_user(self):
    #     user = User("bob", "bobpass")
    #     assert user.username == "bob"

    def test_new_admin(self):
        admin = Admin('bob', 'bobpass', 'bob@mail')
        assert admin.username == "bob"

    def test_new_alumni(self):
        alumni = Alumni('rob', 'robpass', 'rob@mail', '123456789', '1868-333-4444', 'robfname', 'roblname')
        assert alumni.username == 'rob'
    
    def test_new_company(self):
        company = Company('company1', 'company1', 'compass', 'company@mail',  'company_address', 'contact', 'company_website.com')
        assert company.company_name == 'company1'

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = Admin("bob", "bobpass", 'bob@mail')
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", 'email':'bob@mail'})

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = Admin("bob", "bobpass", 'bob@mail')
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", 'email':'bob@mail'})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = Admin("bob", password, 'bob@mail')
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = Admin("bob", password, 'bob@mail')
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = add_admin("bob", "bobpass", 'bob@mail')
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_admin(self):
        add_admin("bob", "bobpass", 'bob@mail')
        admin = add_admin("rick", "bobpass", 'rick@mail')
        assert admin.username == "rick"

    def test_create_alumni(self):
        alumni = add_alumni('rob', 'robpass', 'rob@mail', '123456789', '1868-333-4444', 'robfname', 'roblname')
        assert alumni.username == 'rob'

    def test_create_company(self):
        company = add_company('company1', 'company1', 'compass', 'company@mail',  'company_address', 'contact', 'company_website.com')
        assert company.username == 'company1' and company.company_name == 'company1'

    # cz at the beginning so that it runs after create company
    def test_czadd_listing(self):
        listing = add_listing('listing1', 'listing1 description', 'company1', '8000', 'Full-time', True, True, 'desiredcandidate', 'curepe')
        assert listing.title == 'listing1' and listing.company_name == 'company1'

    def test_subscribe(self):

        alumni = subscribe_action('123456789')
        assert alumni.subscribed == True

    def test_czadd_categories(self):

        alumni = add_categories('123456789', ['Database'])

        assert alumni.get_categories() == ['Database']

    def test_czapply_listing(self):

        alumni = apply_listing('123456789', 1)

        assert get_all_applicants('1')  == [get_alumni('123456789')]


    # def get_all_applicants(self):

    #     applicants = get_all_applicants('1')

    

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([
            {"id":1, "username":"bob", 'email':'bob@mail'},
            {"id":2, "username":"rick", 'email':'rick@mail'},
            {"id":1, "username":"rob", "email":"rob@mail", "alumni_id":123456789, "subscribed":False, "job_category":['Database'], 'contact':'1868-333-4444', 'firstname':'robfname', 'lastname':'roblname'},
            {"id":1, "company_name":"company1", "email":"company@mail", 'company_address':'company_address','contact':'contact',
            'company_website':'company_website.com'}
            ], users_json)

    # def test_create_user(self):
    #     user = create_user("rick", "bobpass")
    #     assert user.username == "rick"

    # def test_get_all_users_json(self):
    #     users_json = get_all_users_json()
    #     self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # # Tests data changes in the database
    # def test_update_user(self):
    #     update_user(1, "ronnie")
    #     user = get_user(1)
    #     assert user.username == "ronnie"
        

