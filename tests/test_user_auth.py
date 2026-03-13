import pytest
from faker import Faker
from pages.home_page import HomePage
from pages.login_signup_page import LoginSignupPage

fake = Faker()

@pytest.fixture
def test_data():
    return {
        "name": fake.name(),
        "email": fake.email(),
        "password": fake.password(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "address": fake.street_address(),
        "state": fake.state(),
        "city": fake.city(),
        "zipcode": fake.zipcode(),
        "mobile": fake.phone_number()
    }

def register_new_user(home_page, login_signup_page, test_data):
    home_page.navigate_to_home()
    home_page.click_signup_login()
    login_signup_page.register_user(test_data["name"], test_data["email"])
    login_signup_page.fill_account_information(
        test_data["password"], test_data["first_name"], test_data["last_name"],
        test_data["address"], test_data["state"], test_data["city"],
        test_data["zipcode"], test_data["mobile"]
    )
    login_signup_page.verify_account_created()

def test_user_registration_and_deletion(page, test_data):
    home_page = HomePage(page)
    login_signup_page = LoginSignupPage(page)
    
    register_new_user(home_page, login_signup_page, test_data)
    home_page.verify_logged_in_as(test_data["name"])
    
    home_page.click_delete_account()
    login_signup_page.verify_account_deleted()

def test_login_correct_credentials(page, test_data):
    home_page = HomePage(page)
    login_signup_page = LoginSignupPage(page)
    
    # Prerequisite: Create user
    register_new_user(home_page, login_signup_page, test_data)
    
    # Logout and login again
    home_page.click_logout()
    home_page.click_signup_login()
    login_signup_page.login_user(test_data["email"], test_data["password"])
    home_page.verify_logged_in_as(test_data["name"])
    
    home_page.click_delete_account()

def test_login_incorrect_credentials(page):
    home_page = HomePage(page)
    login_signup_page = LoginSignupPage(page)
    
    home_page.navigate_to_home()
    home_page.click_signup_login()
    login_signup_page.login_user("invalid_email@example.com", "wrongpassword")
    login_signup_page.verify_error_message("Your email or password is incorrect!")

def test_register_existing_email(page, test_data):
    home_page = HomePage(page)
    login_signup_page = LoginSignupPage(page)
    
    register_new_user(home_page, login_signup_page, test_data)
    home_page.click_logout()
    
    home_page.click_signup_login()
    login_signup_page.register_user(test_data["name"], test_data["email"])
    login_signup_page.verify_error_message("Email Address already exist!")
